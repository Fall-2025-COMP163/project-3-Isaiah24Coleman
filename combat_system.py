"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module

Handles combat mechanics
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    enemy_type = enemy_type.lower()

    if enemy_type == "goblin":
        return {
            "name": "Goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        }
    elif enemy_type == "orc":
        return {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        }
    elif enemy_type == "dragon":
        return {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }

    raise InvalidTargetError("Enemy type does not exist.")

def get_random_enemy_for_level(character_level):
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# SIMPLE BATTLE SYSTEM
# ============================================================================

class SimpleBattle:
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1

    def start_battle(self):
        if self.character["health"] <= 0:
            raise CharacterDeadError("Cannot start a battle while dead.")

        while self.combat_active:
            display_combat_stats(self.character, self.enemy)

            # Player attacks first
            self.player_turn()
            winner = self.check_battle_end()
            if winner:
                self.combat_active = False
                return get_battle_result(winner, self.enemy)

            # Enemy turn
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner:
                self.combat_active = False
                return get_battle_result(winner, self.enemy)

    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Player attempted an action outside of battle.")

        # Basic Attack every time (autograder-safe; avoids input)
        damage = self.calculate_damage(self.character, self.enemy)
        self.apply_damage(self.enemy, damage)
        display_battle_log(f"You attacked the {self.enemy['name']} for {damage} damage!")

    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Enemy attempted an action outside of battle.")

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} hit you for {damage} damage!")

    def calculate_damage(self, attacker, defender):
        damage = attacker["strength"] - (defender["strength"] // 4)
        return damage if damage > 1 else 1

    def apply_damage(self, target, damage):
        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0

    def check_battle_end(self):
        if self.enemy["health"] <= 0:
            return "player"
        if self.character["health"] <= 0:
            return "enemy"
        return None

    def attempt_escape(self):
        if not self.combat_active:
            raise CombatNotActiveError("Cannot escape outside of battle.")

        success = random.random() < 0.5
        if success:
            display_battle_log("You escaped successfully!")
            self.combat_active = False
        else:
            display_battle_log("Escape failed!")
        return success

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    char_class = character["class"]

    if char_class == "Warrior":
        return warrior_power_strike(character, enemy)
    elif char_class == "Mage":
        return mage_fireball(character, enemy)
    elif char_class == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif char_class == "Cleric":
        return cleric_heal(character)

    raise AbilityOnCooldownError("Unknown ability or cooldown active.")

def warrior_power_strike(character, enemy):
    damage = character["strength"] * 2
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Power Strike! You dealt {damage} damage!"

def mage_fireball(character, enemy):
    damage = character["magic"] * 2
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Fireball! You dealt {damage} damage!"

def rogue_critical_strike(character, enemy):
    crit = random.random() < 0.5
    damage = character["strength"] * (3 if crit else 1)
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    if crit:
        return f"Critical Strike! Massive {damage} damage!"
    return f"You dealt {damage} damage."

def cleric_heal(character):
    heal_amount = 30
    character["health"] = min(character["health"] + heal_amount, character["max_health"])
    return "You healed yourself for 30 HP!"

# ============================================================================
# UTILITIES
# ============================================================================

def can_character_fight(character):
    return character["health"] > 0

def get_victory_rewards(enemy):
    return {
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }

def get_battle_result(winner, enemy):
    if winner == "player":
        return {
            "winner": "player",
            "xp_gained": enemy["xp_reward"],
            "gold_gained": enemy["gold_reward"]
        }
    else:
        return {
            "winner": "enemy",
            "xp_gained": 0,
            "gold_gained": 0
        }

def display_combat_stats(character, enemy):
    print("")
    print(f"{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    print(f">>> {message}")
