"""
COMP 163 - Project 3: Quest Chronicles
game data module

Name: Isaiah Coleman

AI Usage: ChatGPT assisted in implementing module integration and safe I/O fallbacks. I also used mt tutor
"""


import re
import os
from custom_exceptions import MissingDataFileError, InvalidDataFormatError, CorruptedDataError

# validate_quest_data(q)
# Ensures that a quest dictionary contains all required fields.
# Checks for the presence of quest_id, title, description, reward_xp, reward_gold, required_level, and prerequisite.
# Validates that reward_xp and reward_gold are integers.
# Ensures required_level is an integer.
# Raises InvalidDataFormatError if any validation fails.
# Returns True if the quest data is valid.
def validate_quest_data(q):
    required_fields = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold", "required_level", "prerequisite"
    ]
    for field in required_fields:
        if field not in q:
            raise InvalidDataFormatError(f"Missing required field: {field}")
    if not isinstance(q["reward_xp"], int) or not isinstance(q["reward_gold"], int):
        raise InvalidDataFormatError("reward_xp and reward_gold must be integers.")
    if not isinstance(q["required_level"], int):
        raise InvalidDataFormatError("required_level must be integer.")
    return True


def validate_item_data(item):
    required_fields = [
        "item_id", "name", "type", "effect", "cost", "description"
    ]
    for field in required_fields:
        if field not in item:
            raise InvalidDataFormatError(f"Missing required field: {field}")
    if not isinstance(item["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer.")
    return True


# _parse_kv_blocks(raw)
# Splits raw text data into blocks separated by empty lines.
# Converts each block into a dictionary of lowercase keys and stripped values.
# Raises InvalidDataFormatError if no blocks are found or lines are improperly formatted.
# Returns a list of parsed dictionaries representing quests or items.
def _parse_kv_blocks(raw):
    blocks = [b.strip() for b in re.split(r"\n\s*\n", raw.strip()) if b.strip()]
    if not blocks:
        raise InvalidDataFormatError("No data blocks found.")
    entries = []
    for block in blocks:
        entry = {}
        for line in block.splitlines():
            if ":" not in line:
                raise InvalidDataFormatError("Invalid line in data block.")
            key, val = line.split(":", 1)
            entry[key.strip().lower()] = val.strip()
        entries.append(entry)
    return entries

# load_quests(filename)
# Reads quest data from a specified text file.
# Raises MissingDataFileError if the file does not exist.
# Raises CorruptedDataError if the file cannot be read.
# Validates that the file is not empty or invalid.
# Parses key-value blocks using _parse_kv_blocks().
# Converts reward_xp, reward_gold, and required_level to integers.
# Ensures each quest has a quest_id and passes validate_quest_data().
# Raises InvalidDataFormatError if any data is missing or incorrectly formatted.
# Returns a dictionary mapping quest_id to quest data.
def load_quests(filename):
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest data file not found: {filename}")
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except Exception as e:
        raise CorruptedDataError(f"Could not read quest data file: {e}")

    if not raw or not raw.strip():
        raise InvalidDataFormatError("Quest data file is empty or invalid.")

    # parse simple KEY: value blocks
    parsed = _parse_kv_blocks(raw)

    quests = {}
    for q in parsed:
        # convert expected numeric fields
        for k in ("reward_xp", "reward_gold", "required_level"):
            if k in q:
                try:
                    q[k] = int(q[k])
                except Exception:
                    raise InvalidDataFormatError(f"Field {k} must be an integer.")
        if "quest_id" not in q:
            raise InvalidDataFormatError("Missing quest_id in quest entry.")
        # validate format (will raise InvalidDataFormatError on problems)
        validate_quest_data(q)
        quests[q["quest_id"]] = q

    if not quests:
        raise InvalidDataFormatError("No valid quests parsed.")
    return quests
# load_items(filename)
# Reads item data from a specified text file.
# Raises MissingDataFileError if the file does not exist.
# Raises CorruptedDataError if the file cannot be read.
# Validates that the file is not empty or invalid.
# Parses key-value blocks using _parse_kv_blocks().
# Converts cost fields to integers.
# Ensures each item has an item_id and passes validate_item_data().
# Raises InvalidDataFormatError if any data is missing or incorrectly formatted.
# Returns a dictionary mapping item_id to item data.
def load_items(filename):
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item data file not found: {filename}")
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except Exception as e:
        raise CorruptedDataError(f"Could not read item data file: {e}")

    if not raw or not raw.strip():
        raise InvalidDataFormatError("Item data file is empty or invalid.")

    parsed = _parse_kv_blocks(raw)

    items = {}
    for it in parsed:
        if "cost" in it:
            try:
                it["cost"] = int(it["cost"])
            except Exception:
                raise InvalidDataFormatError("Item cost must be an integer.")
        if "item_id" not in it:
            raise InvalidDataFormatError("Missing item_id in item entry.")
        # validate format (will raise InvalidDataFormatError on problems)
        validate_item_data(it)
        items[it["item_id"]] = it

    if not items:
        raise InvalidDataFormatError("No valid items parsed.")
    return items
