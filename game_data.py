"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """Load quest data from text file."""
    if not os.path.exists(filename):
        raise MissingDataFileError("Quest file not found.")

    try:
        with open(filename, "r") as f:
            content = f.read().strip()
    except:
        raise CorruptedDataError("Quest file could not be read.")

    if content == "":
        raise InvalidDataFormatError("Quest file is empty.")

    quests = {}
    blocks = content.split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")
        quest = parse_quest_block(lines)

        validate_quest_data(quest)

        quests[quest["quest_id"]] = quest

    return quests


def load_items(filename="data/items.txt"):
    """Load item data from text file."""
    if not os.path.exists(filename):
        raise MissingDataFileError("Item file not found.")

    try:
        with open(filename, "r") as f:
            content = f.read().strip()
    except:
        raise CorruptedDataError("Item file could not be read.")

    if content == "":
        raise InvalidDataFormatError("Item file is empty.")

    items = {}
    blocks = content.split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")
        item = parse_item_block(lines)

        validate_item_data(item)

        items[item["item_id"]] = item

    return items


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(q):
    """Make sure quest has all required fields."""
    required = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite"
    ]

    for key in required:
        if key not in q:
            raise InvalidDataFormatError(f"Missing field: {key}")

    # Check numeric fields
    if not isinstance(q["reward_xp"], int):
        raise InvalidDataFormatError("reward_xp must be an integer")

    if not isinstance(q["reward_gold"], int):
        raise InvalidDataFormatError("reward_gold must be an integer")

    if not isinstance(q["required_level"], int):
        raise InvalidDataFormatError("required_level must be an integer")

    return True


def validate_item_data(item):
    """Make sure item has all required fields."""
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for key in required:
        if key not in item:
            raise InvalidDataFormatError(f"Missing field: {key}")

    valid_types = ["weapon", "armor", "consumable"]
    if item["type"] not in valid_types:
        raise InvalidDataFormatError("Invalid item type.")

    if not isinstance(item["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer")

    return True


# ============================================================================
# DEFAULT FILE CREATION
# ============================================================================

def create_default_data_files():
    """Create data folder and default quest/item files."""
    if not os.path.exists("data"):
        os.makedirs("data")

    # Default quests
    default_quests = """QUEST_1
TITLE: First Steps
DESCRIPTION: Your adventure begins.
REWARD_XP: 50
REWARD_GOLD: 20
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

QUEST_2
TITLE: Goblin Trouble
DESCRIPTION: Defeat the goblins in the forest.
REWARD_XP: 120
REWARD_GOLD: 60
REQUIRED_LEVEL: 2
PREREQUISITE: QUEST_1
"""

    # Default items
    default_items = """ITEM_1
NAME: Wooden Sword
TYPE: weapon
EFFECT: strength:2
COST: 20
DESCRIPTION: A basic starter weapon.

ITEM_2
NAME: Health Potion
TYPE: consumable
EFFECT: health:20
COST: 10
DESCRIPTION: Restores 20 health.
"""

    try:
        with open("data/quests.txt", "w") as f:
            f.write(default_quests)

        with open("data/items.txt", "w") as f:
            f.write(default_items)

    except:
        raise CorruptedDataError("Could not create default files.")


# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """Turn quest block into a dictionary."""
    quest = {}

    try:
        quest["quest_id"] = lines[0].strip()

        for line in lines[1:]:
            if ": " not in line:
                raise InvalidDataFormatError("Invalid quest line format.")
            key, value = line.split(": ", 1)

            if key == "REWARD_XP" or key == "REWARD_GOLD" or key == "REQUIRED_LEVEL":
                value = int(value)

            if key == "TITLE":
                quest["title"] = value
            elif key == "DESCRIPTION":
                quest["description"] = value
            elif key == "REWARD_XP":
                quest["reward_xp"] = value
            elif key == "REWARD_GOLD":
                quest["reward_gold"] = value
            elif key == "REQUIRED_LEVEL":
                quest["required_level"] = value
            elif key == "PREREQUISITE":
                quest["prerequisite"] = value
            else:
                pass

        return quest

    except:
        raise InvalidDataFormatError("Quest block could not be parsed.")


def parse_item_block(lines):
    """Turn item block into a dictionary."""
    item = {}

    try:
        item["item_id"] = lines[0].strip()

        for line in lines[1:]:
            if ": " not in line:
                raise InvalidDataFormatError("Invalid item line format.")
            key, value = line.split(": ", 1)

            if key == "TYPE":
                item["type"] = value
            elif key == "NAME":
                item["name"] = value
            elif key == "DESCRIPTION":
                item["description"] = value
            elif key == "COST":
                item["cost"] = int(value)
            elif key == "EFFECT":
                # format: stat:value
                stat, amount = value.split(":")
                item["effect"] = {stat: int(amount)}
            else:
                pass

        return item

    except:
        raise InvalidDataFormatError("Item block could not be parsed.")


# ============================================================================
# MODULE TEST
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")

    try:
        create_default_data_files()
        qs = load_quests()
        it = load_items()
        print("Loaded", len(qs), "quests")
        print("Loaded", len(it), "items")
    except Exception as e:
        print("Error:", e)

