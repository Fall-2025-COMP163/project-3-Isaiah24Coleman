"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Beginner Version

Name: [Your Name Here]
AI Usage: ChatGPT helped simplify logic and rewrite functions using beginner-level Python.
"""

import os

# =============================================================================
# SIMPLE ERROR MESSAGES (beginner version instead of custom exceptions)
# =============================================================================

ERROR_INVALID_CLASS = "InvalidCharacterClassError"
ERROR_NOT_FOUND = "CharacterNotFoundError"
ERROR_CORRUPTED = "SaveFileCorruptedError"
ERROR_INVALID_DATA = "InvalidSaveDataError"
ERROR_DEAD = "CharacterDeadError"

# =============================================================================
# CHARACTER CREATION
# =============================================================================

def create_character(name, character_class):
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]

    if character_class not in valid_classes:
        raise Exception(ERROR_INVALID_CLASS)

    # Base stats
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

    character = {
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

    return character


# =============================================================================
# SAVING CHARACTER
# =============================================================================

def save_character(character, save_directory="data/save_games"):

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, character["name"] + "_save.txt")

    try:
        with open(filename, "w") as file:
            file.write(f"NAME:{character['name']}\n")
            file.write(f"CLASS:{character['class']}\n")
            file.write(f"LEVEL:{character['level']}\n")
            file.write(f"HEALTH:{character['health']}\n")
            file.write(f"MAX_HEALTH:{character['max_health']}\n")
            file.write(f"STRENGTH:{character['strength']}\n")
            file.write(f"MAGIC:{character['magic']}\n")
            file.write(f"EXPERIENCE:{character['experience']}\n")
            file.write(f"GOLD:{character['gold']}\n")
            file.write("INVENTORY:" + ",".join(character["inventory"]) + "\n")
            file.write("ACTIVE_QUESTS:" + ",".join(character["active_quests"]) + "\n")
            file.write("COMPLETED_QUESTS:" + ",".join(character["completed_quests"]) + "\n")
        return True
    except:
        raise Exception(ERROR_CORRUPTED)


# =============================================================================
# LOADING CHARACTER
# =============================================================================

def load_character(character_name, save_directory="data/save_games"):

    filename = os.path.join(save_directory, character_name + "_save.txt")

    if not os.path.exists(filename):
        raise Exception(ERROR_NOT_FOUND)

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except:
        raise Exception(ERROR_CORRUPTED)

    character = {}

    try:
        for line in lines:
            key, value = line.strip().split(":", 1)

            if key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
                character[key.lower()] = value.split(",") if value else []
            elif key in ["LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH",
                         "MAGIC", "EXPERIENCE", "GOLD"]:
                character[key.lower()] = int(value)
            else:
                character[key.lower()] = value

        validate_character_data(character)

        return character

    except:
        raise Exception(ERROR_INVALID_DATA)


# =============================================================================
# LIST SAVED CHARACTERS
# =============================================================================

def list_saved_characters(save_directory="data/save_games"):

    if not os.path.exists(save_directory):
        return []

    files = os.listdir(save_directory)

    characters = []

    for f in files:
        if f.endswith("_save.txt"):
            characters.append(f.replace("_save.txt", ""))

    return characters


# =============================================================================
# DELETE CHARACTER
# =============================================================================

def delete_character(character_name, save_directory="data/save_games"):

    filename = os.path.join(save_directory, character_name + "_save.txt")

    if not os.path.exists(filename):
        raise Exception(ERROR_NOT_FOUND)

    os.remove(filename)
    return True


# =============================================================================
# CHARACTER OPERATIONS
# =============================================================================

def gain_experience(character, xp_amount):

    if character["health"] <= 0:
        raise Exception(ERROR_DEAD)

    character["experience"] += xp_amount

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    return character


def add_gold(character, amount):

    new_gold = character["gold"] + amount

    if new_gold < 0:
        raise ValueError("Not enough gold")

    character["gold"] = new_gold
    return character["gold"]


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


# =============================================================================
# VALIDATION
# =============================================================================

def validate_character_data(character):

    required = ["name", "class", "level", "health", "max_health",
                "strength", "magic", "experience", "gold",
                "inventory", "active_quests", "completed_quests"]

    for key in required:
        if key not in character:
            raise Exception(ERROR_INVALID_DATA)

    if not isinstance(character["inventory"], list):
        raise Exception(ERROR_INVALID_DATA)

    if not isinstance(character["active_quests"], list):
        raise Exception(ERROR_INVALID_DATA)

    if not isinstance(character["completed_quests"], list):
        raise Exception(ERROR_INVALID_DATA)

    return True


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    hero = create_character("TestHero", "Warrior")
    print(hero)

    save_character(hero)
    print("Saved!")

    loaded = load_character("TestHero")
    print("Loaded:", loaded)

    print("Saved characters:", list_saved_characters())

    print("Deleted:", delete_character("TestHero"))




