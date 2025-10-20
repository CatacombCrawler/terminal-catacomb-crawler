
import ast
from collections import deque

# ---- Legacy name aliases (so old code keeps working) ----
LEGACY_ALIASES = {
    "hp": "health",
    "speed": "speed",        # expect 'speed' as a derived stat in PlayerDatabase (Option 3)
    "attack": "attack",      # expect 'attack' as a derived stat in PlayerDatabase (Option 3)
}


class StatsSystem:
    """
    Computes main & derived stats using PlayerDatabase, class affinities,
    and equipment bonuses. Safe formula evaluator; supports dependencies
    among derived stats.
    """

    def __init__(self, db, class_name="warrior", allocated_main=None, equipment_bonuses=None):
        self.db = db
        self.class_name = class_name
        self.allocated_main = dict(allocated_main or {})
        self.equipment_bonuses = dict(equipment_bonuses or {})

        self._main = {}
        self._derived = {}
        self._dirty = True

        # Whitelisted functions allowed in formulas
        self._funcs = {
            "max": max,
            "min": min,
            "clamp": lambda x, lo, hi: max(lo, min(hi, x)),
        }

    # ---------- public API ----------
    def set_class(self, class_name: str):
        self.class_name = class_name
        self._dirty = True

    def set_allocated_main(self, allocated_main: dict):
        self.allocated_main = dict(allocated_main or {})
        self._dirty = True

    def set_equipment_bonuses(self, equipment_bonuses: dict):
        """equipment_bonuses can include main and/or derived keys."""
        self.equipment_bonuses = dict(equipment_bonuses or {})
        self._dirty = True

    def get_stat(self, name: str):
        key = LEGACY_ALIASES.get(name, name)
        self._recalc_if_needed()
        if key in self._main:
            return self._main[key]
        if key in self._derived:
            return self._derived[key]
        return 0

    def get_base_stat(self, name: str):
        """
        Base main stat (after class bonus + allocation + main_affinity, before equipment).
        For derived stats, returns 0 (use get_stat instead).
        """
        key = LEGACY_ALIASES.get(name, name)
        self._recalc_if_needed()
        # If requested stat is a main stat, return main value without equipment
        if key in self._main:
            eq = self.equipment_bonuses.get(key, 0)
            return max(0, self._main[key] - eq)

        # If requested stat is a derived stat, compute derived value based on
        # mains before equipment (i.e., include class affinities but exclude equipment)
        if key in self.db.STATS["derived"]:
            # Build base mains (remove equipment bonuses from mains)
            base_mains = {}
            for k in self.db.STATS["main"].keys():
                base_val = self._main.get(k, 0) - self.equipment_bonuses.get(k, 0)
                base_mains[k] = base_val

            # Compute derived in topo order using the same logic as _compute_derived
            derived_def = self.db.STATS["derived"]
            cls = self.db.CLASSES[self.class_name]
            d_aff = cls.get("derived_affinity", {})

            order = self._topo_order(list(derived_def.keys()), derived_def)
            env = dict(base_mains)
            derived = {}
            for dkey in order:
                spec = derived_def[dkey]
                expr = spec.get("formula", "0")
                raw_val = self._safe_eval(expr, env)
                raw_val = max(spec["min_value"], min(spec["max_value"], raw_val))
                raw_val *= d_aff.get(dkey, 1.0)
                raw_val = max(spec["min_value"], min(spec["max_value"], raw_val))
                val = int(round(raw_val)) if raw_val > 20 else round(raw_val, 2)
                derived[dkey] = val
                env[dkey] = val

            return derived.get(key, 0)

        return 0

    def get_all_stats(self):
        self._recalc_if_needed()
        merged = dict(self._main)
        merged.update(self._derived)
        return merged

    def get_all_base_stats(self):
        """Return main stats before equipment. Derived stats are computed from formulas."""
        self._recalc_if_needed()
        out = {}
        for k, spec in self.db.STATS["main"].items():
            val = self._main[k] - self.equipment_bonuses.get(k, 0)
            out[k] = max(spec["min_value"], min(spec["max_value"], val))
        return out

    def get_all_equipment_bonuses(self):
        return dict(self.equipment_bonuses)

    def get_stat_breakdown(self, stat_name: str):
        """Lightweight breakdown for UI/tooltips."""
        key = LEGACY_ALIASES.get(stat_name, stat_name)
        self._recalc_if_needed()
        cls = self.db.CLASSES[self.class_name]
        parts = {
            "base_or_formula": None,
            "equipment_bonus": self.equipment_bonuses.get(key, 0),
            "class_derived_affinity": 1.0,
            "total": self.get_stat(stat_name),
        }
        if key in self.db.STATS["main"]:
            base = self._main[key] - parts["equipment_bonus"]
            parts["base_or_formula"] = f"base(main+alloc+class affinity)={base}"
        elif key in self.db.STATS["derived"]:
            parts["base_or_formula"] = self.db.STATS["derived"][key].get("formula", "0")
            parts["class_derived_affinity"] = cls.get("derived_affinity", {}).get(key, 1.0)
        return parts

    # ---------- internal ----------
    def _recalc_if_needed(self):
        if not self._dirty:
            return
        self._compute_main()
        self._compute_derived()
        self._apply_equipment()
        self._dirty = False

    def _compute_main(self):
        stats_def = self.db.STATS["main"]
        cls = self.db.CLASSES[self.class_name]
        start_bonus = cls.get("starting_main_bonus", {})
        aff = cls.get("main_affinity", {})

        main = {}
        for k, spec in stats_def.items():
            base = spec["base_value"]
            val = base + start_bonus.get(k, 0) + self.allocated_main.get(k, 0)
            val = val * aff.get(k, 1.0)
            val = int(round(max(spec["min_value"], min(spec["max_value"], val))))
            main[k] = val
        self._main = main

    def _compute_derived(self):
        derived_def = self.db.STATS["derived"]
        cls = self.db.CLASSES[self.class_name]
        d_aff = cls.get("derived_affinity", {})

        order = self._topo_order(list(derived_def.keys()), derived_def)

        env = dict(self._main)
        derived = {}
        for key in order:
            spec = derived_def[key]
            expr = spec.get("formula", "0")
            raw_val = self._safe_eval(expr, env)
            # clamp
            raw_val = max(spec["min_value"], min(spec["max_value"], raw_val))
            # apply class derived affinity
            raw_val *= d_aff.get(key, 1.0)
            # clamp again
            raw_val = max(spec["min_value"], min(spec["max_value"], raw_val))
            # store (ints for big numbers, keep small values precise if needed)
            val = int(round(raw_val)) if raw_val > 20 else round(raw_val, 2)
            derived[key] = val
            env[key] = val
        self._derived = derived

    def _apply_equipment(self):
        for k, bonus in self.equipment_bonuses.items():
            if k in self._main:
                spec = self.db.STATS["main"][k]
                self._main[k] = int(round(max(spec["min_value"], min(spec["max_value"], self._main[k] + bonus))))
            elif k in self._derived:
                spec = self.db.STATS["derived"][k]
                val = self._derived[k] + bonus
                self._derived[k] = int(round(max(spec["min_value"], min(spec["max_value"], val))))

    # ---- helpers: safe eval & topo ----
    def _safe_eval(self, expr: str, variables: dict):
        def _eval(node):
            if isinstance(node, ast.Expression): return _eval(node.body)
            if isinstance(node, ast.Constant): return node.value
            if isinstance(node, ast.Num): return node.n
            if isinstance(node, ast.BinOp):
                l, r = _eval(node.left), _eval(node.right)
                if isinstance(node.op, ast.Add): return l + r
                if isinstance(node.op, ast.Sub): return l - r
                if isinstance(node.op, ast.Mult): return l * r
                if isinstance(node.op, ast.Div): return l / r
                if isinstance(node.op, ast.FloorDiv): return l // r
                if isinstance(node.op, ast.Mod): return l % r
                if isinstance(node.op, ast.Pow): return l ** r
                raise ValueError("Unsupported operator")
            if isinstance(node, ast.UnaryOp):
                v = _eval(node.operand)
                if isinstance(node.op, ast.UAdd): return +v
                if isinstance(node.op, ast.USub): return -v
                raise ValueError("Unsupported unary operator")
            if isinstance(node, ast.Name):
                if node.id in variables: return variables[node.id]
                raise NameError(f"Unknown var '{node.id}' in formula")
            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name): raise ValueError("Only simple calls allowed")
                fn = node.func.id
                if fn not in self._funcs: raise ValueError(f"Function '{fn}' not allowed")
                args = [_eval(a) for a in node.args]
                return self._funcs[fn](*args)
            raise ValueError("Unsupported expression node")
        return _eval(ast.parse(expr, mode="eval"))

    def _names_in_expr(self, expr: str):
        names = set()
        for n in ast.walk(ast.parse(expr, mode="eval")):
            if isinstance(n, ast.Name):
                names.add(n.id)
        return names

    def _topo_order(self, nodes, derived_def):
        deps = {k: set() for k in nodes}
        for k in nodes:
            refs = self._names_in_expr(derived_def[k].get("formula", "0"))
            deps[k] = {r for r in refs if r in derived_def and r != k}
        indeg = {k: 0 for k in nodes}
        for k in nodes:
            for d in deps[k]:
                indeg[k] += 1
        q = deque([k for k in nodes if indeg[k] == 0])
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in nodes:
                if u in deps[v]:
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        q.append(v)
        return order if len(order) == len(nodes) else nodes