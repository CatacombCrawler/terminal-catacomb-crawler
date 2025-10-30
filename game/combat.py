"""
Combat System - Turn-based combat with initiative and scalable mechanics
"""

import random

class CombatManager:
    """Manages turn-based combat encounters"""
    
    def __init__(self):
        self.in_combat = False
        self.combat_participants = []
        self.current_turn_index = 0
        self.turn_number = 1
        
    def start_combat(self, player, enemies):
        """Initialize a combat encounter"""
        self.in_combat = True
        self.combat_participants = []
        self.current_turn_index = 0
        self.turn_number = 1
        
        # Add player to combat
        player_entry = {
            "entity": player,
            "type": "player",
            "initiative": self.calculate_initiative(player),
            "has_acted": False
        }
        self.combat_participants.append(player_entry)
        
        # Add enemies to combat
        for enemy in enemies:
            enemy_entry = {
                "entity": enemy,
                "type": "enemy", 
                "initiative": self.calculate_initiative(enemy),
                "has_acted": False
            }
            self.combat_participants.append(enemy_entry)
            
        # Sort by initiative (highest first)
        self.combat_participants.sort(key=lambda x: x["initiative"], reverse=True)
        
        return self.get_turn_order_message()
        
    def calculate_initiative(self, entity):
        """Calculate initiative for turn order - scalable for future items/spells"""
        base_initiative = getattr(entity, 'speed', 10)
        
        # Add randomness
        roll = random.randint(1, 20)
        
        # Future expansion points:
        # - Item bonuses: initiative += entity.get_initiative_bonus()
        # - Spell effects: initiative += entity.get_active_spell_bonus("initiative")
        # - Status effects: if entity.has_status("haste"): initiative += 5
        
        return base_initiative + roll
        
    def get_current_actor(self):
        """Get the entity whose turn it is"""
        if not self.in_combat or not self.combat_participants:
            return None
            
        return self.combat_participants[self.current_turn_index]
        
    def is_player_turn(self):
        """Check if it's the player's turn"""
        current = self.get_current_actor()
        return current and current["type"] == "player"
        
    def end_turn(self):
        """End current entity's turn and advance to next"""
        if not self.in_combat:
            return None
            
        # Mark current actor as having acted
        self.combat_participants[self.current_turn_index]["has_acted"] = True
        
        # Move to next participant
        self.current_turn_index += 1
        
        # Check if round is complete
        if self.current_turn_index >= len(self.combat_participants):
            return self.end_round()
            
        return None
        
    def end_round(self):
        """End the current round and start a new one"""
        self.turn_number += 1
        self.current_turn_index = 0
        
        # Reset "has_acted" flags
        for participant in self.combat_participants:
            participant["has_acted"] = False
            
        # Remove dead enemies from combat
        self.combat_participants = [p for p in self.combat_participants 
                                    if p["type"] == "player" or p["entity"].is_alive()]
        
        # Check if combat should end
        if self.should_end_combat():
            return self.end_combat()
            
        return f"Round {self.turn_number} begins!"
        
    def should_end_combat(self):
        """Check if combat should end"""
        player_alive = any(p["type"] == "player" and p["entity"].hp > 0 
                           for p in self.combat_participants)
        enemies_alive = any(p["type"] == "enemy" and p["entity"].is_alive() 
                            for p in self.combat_participants)
        
        return not player_alive or not enemies_alive
        
    def end_combat(self):
        """End the combat encounter"""
        self.in_combat = False
        
        # Determine victory/defeat
        player_alive = any(p["type"] == "player" and p["entity"].hp > 0 
                           for p in self.combat_participants)
        
        self.combat_participants = []
        self.current_turn_index = 0
        
        if player_alive:
            return "Combat ended - Victory!"
        else:
            return "Combat ended - Defeat!"
            
    def get_turn_order_message(self):
        """Get a message showing turn order"""
        order = []
        for i, participant in enumerate(self.combat_participants):
            name = participant["entity"].name if hasattr(participant["entity"], 'name') else str(participant["entity"])
            initiative = participant["initiative"]
            marker = " <-- CURRENT" if i == self.current_turn_index else ""
            order.append(f"{name} (Initiative: {initiative}){marker}")
            
        return "Combat begins! Turn order:\n" + "\n".join(order)
        
    def get_combat_status(self):
        """Get current combat status"""
        if not self.in_combat:
            return "Not in combat"
            
        current = self.get_current_actor()
        if not current:
            return "Combat error"
            
        name = current["entity"].name if hasattr(current["entity"], 'name') else str(current["entity"])
        return f"Round {self.turn_number} - {name}'s turn"


class CombatAction:
    """Represents a combat action that can be taken during a turn"""

    def __init__(self, name, action_type, target_type="enemy"):
        self.name = name
        self.action_type = action_type
        self.target_type = target_type

    def can_use(self, actor):
        """Check if the actor can use this action - scalable for future mechanics"""
        
        # This logic is specifically for spear_dash
        if self.action_type == "spear_dash":
            equipped_weapon = None
            if hasattr(actor, 'equipment') and 'main_hand' in actor.equipment:
                equipped_weapon = actor.equipment['main_hand']

            # Check if the weapon exists and is the 'iron_spear'
            # Assuming your Item object has an 'item_id' property (e.g., 'iron_spear')
            if equipped_weapon and hasattr(equipped_weapon, 'item_id') and equipped_weapon.item_id == 'iron_spear':
                return True # Yes, they can use it
            else:
                return False # No spear, no dash
        
        # All other actions are usable by default for now
        # Future expansion:
        # - Check mana/stamina costs
        # - Check item availability 
        # - Check cooldowns
        # - Check status effects
        return True
        
    def execute(self, actor, target=None):
        """Execute the combat action - scalable for future mechanics"""
        if self.action_type == "attack":
            return self.execute_attack(actor, target)
        elif self.action_type == "defend":
            return self.execute_defend(actor)
        
        # Check for "spear_dash"
        elif self.action_type == "spear_dash":
            return self.execute_spear_dash(actor, target)
            
    def execute_attack(self, attacker, target):
        """Execute an attack action"""
        if not target or not target.is_alive():
            return {"success": False, "message": "Invalid target"}
        
        # Check if attacker is a monster with advanced attack system
        if hasattr(attacker, 'attack_player') and hasattr(attacker, 'data'):
            monster_attack_result = attacker.attack_player(target)
            
            exp_gained = 0
            if hasattr(target, 'gain_exp') and monster_attack_result.get('player_died') and hasattr(attacker, 'exp_reward'):
                target.gain_exp(attacker.exp_reward)
                exp_gained = attacker.exp_reward
            
            combat_result = {
                "success": True,
                "action": "attack",
                "attacker": monster_attack_result.get("attacker", attacker.name if hasattr(attacker, 'name') else "Unknown"),
                "attack_name": monster_attack_result.get("attack_name", "Attack"),
                "damage": monster_attack_result.get("damage", 0),
                "deflected": monster_attack_result.get("deflected", 0),
                "hit": monster_attack_result.get("hit", True),
                "description": monster_attack_result.get("description", ""),
                "target_died": monster_attack_result.get("player_died", False),
                "special_effects": monster_attack_result.get("special_effects"),
                "exp_gained": exp_gained
            }
            return combat_result
        # Check if attacker is a player with enhanced attack system
        elif hasattr(attacker, 'attack_enemy') and hasattr(attacker, 'accuracy'):
            player_attack_result = attacker.attack_enemy(target)
            
            combat_result = {
                "success": True,
                "action": "attack",
                "attacker": player_attack_result.get("attacker", attacker.name if hasattr(attacker, 'name') else "Unknown"),
                "target": player_attack_result.get("target", target.name if hasattr(target, 'name') else "Enemy"),
                "damage": player_attack_result.get("damage", 0),
                "deflected": player_attack_result.get("deflected", 0),
                "hit": player_attack_result.get("hit", True),
                "critical": player_attack_result.get("critical", False),
                "parried": player_attack_result.get("parried", False),
                "target_died": player_attack_result.get("enemy_died", False),
                "exp_gained": player_attack_result.get("exp_gained", 0),
                "leveled_up": player_attack_result.get("leveled_up", False),
                "message": player_attack_result.get("message", "Attack completed")
            }
            return combat_result
        else:
            # Use basic attack system for player or non-monster entities
            base_damage = attacker.attack
            damage_roll = random.randint(-2, 3)
            
            total_damage = max(1, base_damage + damage_roll)
            
            damage_result = target.take_damage(total_damage)
            target_died = damage_result.get("died", False) if isinstance(damage_result, dict) else damage_result
            
            exp_gained = 0
            if hasattr(attacker, 'gain_exp') and target_died and hasattr(target, 'exp_reward'):
                monster_level = getattr(target, 'level', None)
                original_exp = target.exp_reward
                attacker.gain_exp(target.exp_reward, monster_level)
                
                if monster_level is not None and monster_level > attacker.level:
                    level_difference = monster_level - attacker.level
                    multiplier = 2 ** level_difference
                    exp_gained = int(original_exp * multiplier)
                else:
                    exp_gained = original_exp
                    
            return {
                "success": True,
                "action": "attack",
                "attacker": attacker.name if hasattr(attacker, 'name') else "Unknown",
                "target": target.name if hasattr(target, 'name') else "Enemy",
                "damage": total_damage,
                "hit": True,
                "target_died": target_died,
                "exp_gained": exp_gained
            }
            
    def execute_spear_dash(self, attacker, target):
        """Execute a spear dash attack - this calls a special method on the player"""
        if not target or not target.is_alive():
            return {"success": False, "message": "Invalid target"}
            
        # We assume the player (attacker) has a new method called 'spear_dash_attack'
        # This keeps the logic consistent with your 'attack_enemy' method
        if hasattr(attacker, 'spear_dash_attack'):
            # Use player's special spear dash system
            dash_result = attacker.spear_dash_attack(target)
            
            # Convert the result to the combat system format
            combat_result = {
                "success": True,
                "action": "spear_dash", # Identify this as a special action
                "attacker": dash_result.get("attacker", attacker.name if hasattr(attacker, 'name') else "Unknown"),
                "target": dash_result.get("target", target.name if hasattr(target, 'name') else "Enemy"),
                "damage": dash_result.get("damage", 0),
                "hit": dash_result.get("hit", True),
                "critical": dash_result.get("critical", False), # Maybe dashes can crit?
                "target_died": dash_result.get("enemy_died", False),
                "exp_gained": dash_result.get("exp_gained", 0),
                "leveled_up": dash_result.get("leveled_up", False),
                "message": dash_result.get("message", "You dash forward!")
            }
            return combat_result
        else:
            # Fallback if the 'spear_dash_attack' method is missing
            return {"success": False, "message": "Spear Dash ability not implemented on actor."}
        
    def execute_defend(self, defender):
        """Execute a defend action - reduces incoming damage next turn"""
        return {
            "success": True,
            "action": "defend", 
            "defender": defender.name if hasattr(defender, 'name') else "Unknown",
            "message": f"{defender.name if hasattr(defender, 'name') else 'Unknown'} takes a defensive stance"
        }


# Available combat actions
COMBAT_ACTIONS = {
    "attack": CombatAction("Attack", "attack", "enemy"),
    "defend": CombatAction("Defend", "defend", "self"),
    "spear_dash": CombatAction("Spear Dash", "spear_dash", "enemy"), # <-- ADDED!
    # Future actions:
    # "heal": CombatAction("Heal", "item", "self"),
    # "fireball": CombatAction("Fireball", "spell", "area"),
}
