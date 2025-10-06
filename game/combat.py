"""
Combat System - Turn-based combat with initiative and scalable mechanics
Enhanced with Status Effect system contribution
"""

import random

class StatusEffect:
    """Represents a status effect applied to an entity"""
    
    def __init__(self, name, duration, damage_per_turn=0, description=""):
        self.name = name
        self.duration = duration
        self.damage_per_turn = damage_per_turn
        self.description = description
        
    def apply_effect(self, target):
        """Apply effect for this turn"""
        result = {}
        if self.damage_per_turn > 0:
            damage_result = target.take_damage(self.damage_per_turn)
            target_died = damage_result.get("died", False) if isinstance(damage_result, dict) else damage_result
            result = {
                "effect": self.name,
                "damage": self.damage_per_turn,
                "target_died": target_died
            }
        self.duration -= 1
        return result

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
            "has_acted": False,
            "status_effects": []
        }
        self.combat_participants.append(player_entry)
        
        # Add enemies to combat
        for enemy in enemies:
            enemy_entry = {
                "entity": enemy,
                "type": "enemy", 
                "initiative": self.calculate_initiative(enemy),
                "has_acted": False,
                "status_effects": []
            }
            self.combat_participants.append(enemy_entry)
            
        # Sort by initiative (highest first)
        self.combat_participants.sort(key=lambda x: x["initiative"], reverse=True)
        
        return self.get_turn_order_message()
        
    def calculate_initiative(self, entity):
        """Calculate initiative for turn order - scalable for future items/spells"""
        base_initiative = getattr(entity, 'speed', 10)
        roll = random.randint(1, 20)
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
        
        current_actor_entry = self.combat_participants[self.current_turn_index]
        
        # Apply status effects at the end of their turn
        self.process_status_effects(current_actor_entry)
        
        # Mark current actor as having acted
        current_actor_entry["has_acted"] = True
        
        # Move to next participant
        self.current_turn_index += 1
        
        # Check if round is complete
        if self.current_turn_index >= len(self.combat_participants):
            return self.end_round()
            
        return None
        
    def process_status_effects(self, actor_entry):
        """Apply all active status effects to the actor"""
        actor = actor_entry["entity"]
        remaining_effects = []
        messages = []
        for effect in actor_entry.get("status_effects", []):
            result = effect.apply_effect(actor)
            if result:
                messages.append(f"{actor.name if hasattr(actor, 'name') else 'Entity'} suffers {result.get('damage',0)} damage from {effect.name}")
            if effect.duration > 0:
                remaining_effects.append(effect)
        actor_entry["status_effects"] = remaining_effects
        return messages
        
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
    """Represents a combat action that can be taken"""
    
    def __init__(self, name, action_type, target_type="enemy"):
        self.name = name
        self.action_type = action_type
        self.target_type = target_type
        
    def can_use(self, actor):
        """Check if actor can use this action"""
        return True
        
    def execute(self, actor, target=None):
        """Execute the combat action"""
        if self.action_type == "attack":
            return self.execute_attack(actor, target)
        elif self.action_type == "defend":
            return self.execute_defend(actor)
        elif self.action_type == "status_effect":
            return self.apply_status_effect(actor, target)
        
    def execute_attack(self, attacker, target):
        """Simplified attack logic (kept original as-is)"""
        if not target or not target.is_alive():
            return {"success": False, "message": "Invalid target"}
        base_damage = getattr(attacker, "attack", 5)
        damage_roll = random.randint(-2, 3)
        total_damage = max(1, base_damage + damage_roll)
        damage_result = target.take_damage(total_damage)
        target_died = damage_result.get("died", False) if isinstance(damage_result, dict) else damage_result
        return {
            "success": True,
            "action": "attack",
            "attacker": getattr(attacker, 'name', 'Unknown'),
            "target": getattr(target, 'name', 'Enemy'),
            "damage": total_damage,
            "hit": True,
            "target_died": target_died
        }
        
    def execute_defend(self, defender):
        """Execute a defend action"""
        return {
            "success": True,
            "action": "defend",
            "defender": getattr(defender, 'name', 'Unknown'),
            "message": f"{getattr(defender, 'name', 'Unknown')} takes a defensive stance"
        }
        
    def apply_status_effect(self, actor, target):
        """Apply a status effect (new contribution)"""
        if not target or not target.is_alive():
            return {"success": False, "message": "Invalid target"}
        
        # Example: apply poison for 3 turns, 2 damage per turn
        poison = StatusEffect("Poison", duration=3, damage_per_turn=2, description="Deals damage over time")
        # Find target entry in combat manager
        if hasattr(actor, "combat_manager"):
            for participant in actor.combat_manager.combat_participants:
                if participant["entity"] == target:
                    participant["status_effects"].append(poison)
                    return {
                        "success": True,
                        "action": "status_effect",
                        "effect": "Poison",
                        "target": getattr(target, "name", "Enemy"),
                        "message": f"{getattr(target, 'name', 'Enemy')} is poisoned!"
                    }
        return {"success": False, "message": "Could not apply status effect"}


# Available combat actions
COMBAT_ACTIONS = {
    "attack": CombatAction("Attack", "attack", "enemy"),
    "defend": CombatAction("Defend", "defend", "self"),
    "poison": CombatAction("Poison", "status_effect", "enemy"),
}
