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
    """Represents a combat action that can be taken"""
    
    def __init__(self, name, action_type, target_type="enemy"):
        self.name = name
        self.action_type = action_type  # "attack", "defend", "item", "spell", etc.
        self.target_type = target_type  # "enemy", "self", "ally", "area"
        
    def can_use(self, actor):
        """Check if actor can use this action - extensible for items/mana/cooldowns"""
        # Future expansion:
        # - Check mana/stamina costs
        # - Check item availability  
        # - Check cooldowns
        # - Check status effects
        return True
        
    def execute(self, actor, target=None):
        """Execute the combat action - returns result dict"""
        if self.action_type == "attack":
            return self.execute_attack(actor, target)
        elif self.action_type == "defend":
            return self.execute_defend(actor)
        # Future actions: heal, cast_spell, use_item, etc.
        
    def execute_attack(self, attacker, target):
        """Execute an attack action"""
        if not target or not target.is_alive():
            return {"success": False, "message": "Invalid target"}
        
        # Check if attacker is a monster with advanced attack system
        if hasattr(attacker, 'attack_player') and hasattr(attacker, 'data'):
            # Use monster's sophisticated attack system
            monster_attack_result = attacker.attack_player(target)
            
            # Handle experience gain for player targets
            exp_gained = 0
            if hasattr(target, 'gain_exp') and monster_attack_result.get('player_died') and hasattr(attacker, 'exp_reward'):
                target.gain_exp(attacker.exp_reward)
                exp_gained = attacker.exp_reward
            
            # Convert monster attack result to combat system format
            # Note: We don't include "target" key for monster attacks to ensure UI
            # properly identifies them as enemy attacks for rich formatting
            return {
                "success": True,
                "action": "attack",
                "attacker": monster_attack_result.get("attacker", attacker.name if hasattr(attacker, 'name') else "Unknown"),
                "attack_name": monster_attack_result.get("attack_name", "Attack"),
                "damage": monster_attack_result.get("damage", 0),
                "hit": monster_attack_result.get("hit", True),
                "description": monster_attack_result.get("description", ""),
                "target_died": monster_attack_result.get("player_died", False),
                "special_effects": monster_attack_result.get("special_effects"),
                "exp_gained": exp_gained
            }
        else:
            # Use basic attack system for player or non-monster entities
            # Calculate damage with potential modifiers
            base_damage = attacker.attack
            damage_roll = random.randint(-2, 3)
            
            # Future expansion points:
            # - Weapon bonuses: base_damage += attacker.weapon.damage if attacker.weapon
            # - Critical hits: if random.randint(1, 20) >= 18: damage *= 2
            # - Status effects: if attacker.has_status("rage"): damage += 5
            
            total_damage = max(1, base_damage + damage_roll)
            
            # Apply damage
            target_died = target.take_damage(total_damage)
            
            # Handle experience gain for player
            exp_gained = 0
            if hasattr(attacker, 'gain_exp') and target_died and hasattr(target, 'exp_reward'):
                attacker.gain_exp(target.exp_reward)
                exp_gained = target.exp_reward
                
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
        
    def execute_defend(self, defender):
        """Execute a defend action - reduces incoming damage next turn"""
        # Future: Add temporary defense bonus
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
    # Future actions:
    # "heal": CombatAction("Heal", "item", "self"),
    # "fireball": CombatAction("Fireball", "spell", "area"),
}
