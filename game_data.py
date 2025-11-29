"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: ChatGPT used for debugging & formatting assistance.
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
    """Load all quests from text file."""
    if not os.path.exists(filename):
        raise MissingDataFileError("Quest file not found.")

    try:
        with open(filename, "r") as f:
            raw = f.read().strip()
    except Exception:
        raise CorruptedDataError("Quest file could not be read.")

    if raw == "":
        raise InvalidDataFormatError("Quest file is empty.")

    quests = {}
    blocks = [b.strip() for b in raw.split("\n\n") if b.strip()]

    for block in blocks:
        lines = block.split("\n")
        quest = parse_quest_block(lines)
        validate_quest_data(quest)
        quests[quest["quest_id"]] = quest

    return quests


def load_items(filename="data/items.txt"):
    """Load all items from text file."""
    if not os.path.exists(filename):
        raise MissingDataFileError("Item file not found.")

    try:
        with open(filename, "r") as f:
            raw = f.read().strip()
    except Exception:
        raise CorruptedDataError("Item file could not be read.")

    if raw == "":
        raise InvalidDataFormatError("Item file is empty.")

    items = {}
    blocks = [b.strip() for b in raw.split("\n\n") if b.strip()]

    for block in blocks:
        lines = block.split("\n")
        item = parse_item_block(lines)
        validate_item_data(item)
        items[item["item_id"]] = item

    return items


# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_data(q):
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

    if not isinstance(q["reward_xp"], int):
        raise InvalidDataFormatError("reward_xp must be an integer")

    if not isinstance(q["reward_gold"], int):
        raise InvalidDataFormatError("reward_gold must be an integer")

    if not isinstance(q["required_level"], int):
        raise InvalidDataFormatError("required_level must be an integer")

    return True


def validate_item_data(item):
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for key in required:
        if key not in item:
            raise InvalidDataFormatError(f"Missing field: {key}")

    valid_types = ["weapon", "armor", "consumable"]
    if item["type"] not in valid_types:
        raise InvalidDataFormatError("Invalid item type.")

    if not isinstance(item["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer")

    if not isinstance(item["effect"], dict):
        raise InvalidDataFormatError("Effect must be a dictionary.")

    return True


# ============================================================================
# DEFAULT FILE CREATION
# ============================================================================

def create_default_data_files():
    """Create /data folder and default quest/item text files."""
    if not os.path.exists("data"):
        os.makedirs("data")

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
    except Exception:
        raise CorruptedDataError("Could not create default data files.")


# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """Convert quest lines into a dict."""
    if len(lines) == 0:
        raise InvalidDataFormatError("Quest block is empty.")

    quest = {}

    try:
        quest["quest_id"] = lines[0].strip()

        for line in lines[1:]:
            if ": " not in line:
                raise InvalidDataFormatError("Invalid quest line format.")

            key, value = line.split(": ", 1)

            if key == "TITLE":
                quest["title"] = value
            elif key == "DESCRIPTION":
                quest["description"] = value
            elif key == "REWARD_XP":
                quest["reward_xp"] = int(value)
            elif key == "REWARD_GOLD":
                quest["reward_gold"] = int(value)
            elif key == "REQUIRED_LEVEL":
                quest["required_level"] = int(value)
            elif key == "PREREQUISITE":
                quest["prerequisite"] = value

        return quest

    except Exception:
        raise InvalidDataFormatError("Quest block could not be parsed.")


def parse_item_block(lines):
    """Convert item lines into a dict."""
    if len(lines) == 0:
        raise InvalidDataFormatError("Item block is empty.")

    item = {}

    try:
        item["item_id"] = lines[0].strip()

        for line in lines[1:]:
            if ": " not in line:
                raise InvalidDataFormatError("Invalid item line format.")

            key, value = line.split(": ", 1)

            if key == "NAME":
                item["name"] = value
            elif key == "TYPE":
                item["type"] = value
            elif key == "DESCRIPTION":
                item["description"] = value
            elif key == "COST":
                item["cost"] = int(value)
            elif key == "EFFECT":
                # stat:value format
                if ":" not in value:
                    raise InvalidDataFormatError("Effect format must be stat:value")

                stat, amount = value.split(":")
                item["effect"] = {stat.strip(): int(amount)}

        return item

    except Exception:
        raise InvalidDataFormatError("Item block could not be parsed.")


# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE SELF TEST ===")
    try:
        create_default_data_files()
        qs = load_quests()
        it = load_items()
        print("Loaded quests:", len(qs))
        print("Loaded items:", len(it))
    except Exception as e:
        print("Error:", e)
