import re
import os
from custom_exceptions import MissingDataFileError, InvalidDataFormatError, CorruptedDataError

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
