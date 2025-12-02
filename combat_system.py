"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module

Isaiah Coleman

Had to use Ai tp clean up code as well as my upswing tutor

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
#This section defines all enemy types used in the game, including their stats, rewards, and how they are generated based on player level. 
#It sets the foundation for every encounter by specifying what enemies exist and what attributes they bring into battle.
#
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
    # create_enemy lowercases internally, but we keep the strings explicit
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ============================================================================
# SIMPLE BATTLE SYSTEM
#This section contains the full logic for running a turn-based fight between the player and an enemy. 
#It manages the battle loop, handles turns, calculates damage, checks win/loss conditions, and controls when combat starts or ends. 
#It forms the core gameplay loop of fighting.
# ============================================================================

class SimpleBattle:
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1

    def start_battle(self):
        if self.character.get("health", 0) <= 0:
            raise CharacterDeadError("Cannot start a battle while dead.")

        # Basic loop — deterministic for tests (no input)
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

        # Basic Attack
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
        # Simple formula, ensures at least 1 damage
        damage = attacker.get("strength", 1) - (defender.get("strength", 0) // 4)
        return damage if damage > 1 else 1

    def apply_damage(self, target, damage):
        target["health"] = max(0, target.get("health", 0) - damage)

    def check_battle_end(self):
        if self.enemy.get("health", 0) <= 0:
            return "player"
        if self.character.get("health", 0) <= 0:
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
#This section handles all class-specific special moves—like warrior power strikes, mage fireballs, rogue crits, and cleric heals. 
#It determines which ability is allowed, applies effects to enemies or the player, and ensures abilities behave differently based on class.


# ============================================================================

def use_special_ability(character, enemy=None):
    """
    Use the character's special ability.
    `enemy` may be None for heal-like abilities (cleric).
    """
    char_class = str(character.get("class", "")).lower()

    if char_class == "warrior":
        if enemy is None:
            raise InvalidTargetError("No enemy specified for warrior ability.")
        return warrior_power_strike(character, enemy)
    elif char_class == "mage":
        if enemy is None:
            raise InvalidTargetError("No enemy specified for mage ability.")
        return mage_fireball(character, enemy)
    elif char_class == "rogue":
        if enemy is None:
            raise InvalidTargetError("No enemy specified for rogue ability.")
        return rogue_critical_strike(character, enemy)
    elif char_class == "cleric":
        return cleric_heal(character)

    # Unknown class — tests expect an InvalidTargetError rather than a cooldown error
    raise InvalidTargetError("Unknown ability.")


def warrior_power_strike(character, enemy):
    damage = character.get("strength", 1) * 2
    enemy["health"] = max(0, enemy.get("health", 0) - damage)
    return f"Power Strike! You dealt {damage} damage!"


def mage_fireball(character, enemy):
    damage = character.get("magic", 1) * 2
    enemy["health"] = max(0, enemy.get("health", 0) - damage)
    return f"Fireball! You dealt {damage} damage!"


def rogue_critical_strike(character, enemy):
    crit = random.random() < 0.5
    damage = character.get("strength", 1) * (3 if crit else 1)
    enemy["health"] = max(0, enemy.get("health", 0) - damage)
    if crit:
        return f"Critical Strike! Massive {damage} damage!"
    return f"You dealt {damage} damage."


def cleric_heal(character):
    heal_amount = 30
    character["health"] = min(character.get("health", 0) + heal_amount, character.get("max_health", 0))
    return f"You healed yourself for {heal_amount} HP!"


# ============================================================================
# UTILITIES
#  section includes helper functions used throughout combat, such as checking if a character can fight, calculating rewards, formatting battle results, and printing combat information. 
#These are small but essential tools that support the main combat system.
# ============================================================================

def can_character_fight(character):
    return character.get("health", 0) > 0


def get_victory_rewards(enemy):
    return {
        "xp": int(enemy.get("xp_reward", 0)),
        "gold": int(enemy.get("gold_reward", 0))
    }


def get_battle_result(winner, enemy):
    if winner == "player":
        return {
            "winner": "player",
            "xp_gained": int(enemy.get("xp_reward", 0)),
            "gold_gained": int(enemy.get("gold_reward", 0))
        }
    else:
        return {
            "winner": "enemy",
            "xp_gained": 0,
            "gold_gained": 0
        }


def display_combat_stats(character, enemy):
    # Minimal output useful for debugging; tests ignore prints
    print("")
    print(f"{character.get('name', 'Hero')}: HP={character.get('health', 0)}/{character.get('max_health', 0)}")
    print(f"{enemy.get('name', 'Enemy')}: HP={enemy.get('health', 0)}/{enemy.get('max_health', 0)}")


def display_battle_log(message):
    # Minimal output; tests don't assert on prints
    print(f">>> {message}")

