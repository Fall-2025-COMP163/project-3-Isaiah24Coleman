# (Full file content, same as original up to the end of the module)
"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ==============================================================================
# CHARACTER CREATION
# ==============================================================================

def create_character(name, character_class):
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]

    if character_class not in valid_classes:
        raise InvalidCharacterClassError("Invalid character class.")

    # Assign base stats
    if character_class == "Warrior":
        health = 120
        strength = 15
        magic = 5
    elif character_class == "Mage":
        health = 80
        strength = 8
        magic = 20
    elif character_class == "Rogue":
        health = 90
        strength = 12
        magic = 10
    elif character_class == "Cleric":
        health = 100
        strength = 10
        magic = 15

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": health,
        "max_health": health,
        "strength": strength,
        "magic": magic,
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

# ==============================================================================
# SAVE CHARACTER
# ==============================================================================

def save_character(character, save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w") as file:
            for key in [
                "name", "class", "level", "health", "max_health",
                "strength", "magic", "experience", "gold"
            ]:
                file.write(f"{key.upper()}:{character[key]}\n")

            file.write("INVENTORY:" + ",".join(character["inventory"]) + "\n")
            file.write("ACTIVE_QUESTS:" + ",".join(character["active_quests"]) + "\n")
            file.write("COMPLETED_QUESTS:" + ",".join(character["completed_quests"]) + "\n")

    except Exception:
        raise SaveFileCorruptedError("Unable to save character file.")

    return True

# ==============================================================================
# LOAD CHARACTER
# ==============================================================================

def load_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("Save file not found.")

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except Exception:
        raise SaveFileCorruptedError("Save file could not be read.")

    character = {}

    try:
        for line in lines:
            if ":" not in line:
                raise InvalidSaveDataError("Invalid save data format.")
            key, value = line.strip().split(":", 1)

            key = key.lower()

            if key in ["inventory", "active_quests", "completed_quests"]:
                character[key] = value.split(",") if value else []
            elif key in [
                "level", "health", "max_health",
                "strength", "magic", "experience", "gold"
            ]:
                character[key] = int(value)
            else:
                character[key] = value
    except Exception:
        raise InvalidSaveDataError("Save file contains invalid data.")

    validate_character_data(character)

    return character

# ==============================================================================
# LIST SAVED CHARACTERS
# ==============================================================================

def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []

    characters = []

    for file in os.listdir(save_directory):
        if file.endswith("_save.txt"):
            characters.append(file.replace("_save.txt", ""))

    return characters

# ==============================================================================
# DELETE CHARACTER
# ==============================================================================

def delete_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("Character save file does not exist.")

    os.remove(filename)
    return True

# ==============================================================================
# CHARACTER OPERATIONS
# ==============================================================================

def gain_experience(character, xp_amount):
    if character["health"] <= 0:
        raise CharacterDeadError("Cannot gain experience while dead.")

    character["experience"] += xp_amount

    # Level-up logic
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    return character

def add_gold(character, amount):
    new_total = character["gold"] + amount

    if new_total < 0:
        raise ValueError("Not enough gold.")

    character["gold"] = new_total
    return new_total

def heal_character(character, amount):
    old_health = character["health"]
    character["health"] = min(character["health"] + amount, character["max_health"])
    return character["health"] - old_health

def is_character_dead(character):
    return character["health"] <= 0

def revive_character(character):
    if character["health"] > 0:
        return False

    character["health"] = character["max_health"] // 2
    return True

# ==============================================================================
# VALIDATION
# ==============================================================================

def validate_character_data(character):
    required = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for key in required:
        if key not in character:
            raise InvalidSaveDataError("Missing required save data.")

    if not isinstance(character["inventory"], list):
        raise InvalidSaveDataError("Invalid inventory format.")

    if not isinstance(character["active_quests"], list):
        raise InvalidSaveDataError("Invalid quest data.")

    if not isinstance(character["completed_quests"], list):
        raise InvalidSaveDataError("Invalid quest data.")

    return True
