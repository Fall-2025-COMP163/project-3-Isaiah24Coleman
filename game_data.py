# (Only the validate_item_data function is adjusted below; rest of file unchanged)
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

# ... (other functions unchanged) ...
from custom_exceptions import InvalidDataFormatError

def load_quests(filename):
    # ... (file reading code)
    if not valid_format(data):
        raise InvalidDataFormatError("Quest data is not properly formatted.")
    # ...

def load_items(filename):
    # TODO: Implement file reading and parsing
    return {}

def validate_quest_data(quest):
    # TODO: Add full quest validation logic
    required = ["quest_id", "title", "description", "reward_xp", "reward_gold", "required_level", "prerequisite"]
    for key in required:
        if key not in quest:
            raise InvalidDataFormatError(f"Missing field: {key}")
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

    # Accept either a dict or a "stat:amount" string for effect
    if isinstance(item["effect"], dict):
        # ensure values are ints
        for v in item["effect"].values():
            if not isinstance(v, int):
                raise InvalidDataFormatError("Effect values must be integers.")
    elif isinstance(item["effect"], str):
        if ":" not in item["effect"]:
            raise InvalidDataFormatError("Effect must be 'stat:amount' string or a dict.")
        stat, amount = item["effect"].split(":", 1)
        try:
            int(amount)
        except Exception:
            raise InvalidDataFormatError("Effect amount must be an integer.")
    else:
        raise InvalidDataFormatError("Effect must be a dictionary or 'stat:number' string.")

    return True

# ... (rest of file unchanged) ...
