"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """Add an item to the inventory."""
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full.")

    character["inventory"].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    """Remove a single instance of an item."""
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory.")

    character["inventory"].remove(item_id)
    return True


def has_item(character, item_id):
    """Check if character has one of an item."""
    return item_id in character["inventory"]


def count_item(character, item_id):
    """Count duplicates of a specific item."""
    return character["inventory"].count(item_id)


def get_inventory_space_remaining(character):
    """How many items can still fit."""
    return MAX_INVENTORY_SIZE - len(character["inventory"])


def clear_inventory(character):
    """Remove all items and return what was removed."""
    removed = character["inventory"][:]
    character["inventory"] = []
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """Use a consumable item such as potions."""
    if not has_item(character, item_id):
        raise ItemNotFoundError("Item not in inventory.")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Only consumables can be used.")

    stat, amount = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, amount)

    remove_item_from_inventory(character, item_id)
    return f"Used {item_data['name']} (+{amount} {stat})."


# ============================================================================
# EQUIPPING WEAPONS
# ============================================================================

def equip_weapon(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError("Weapon not in inventory.")

    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")

    # Unequip current weapon
    if character.get("equipped_weapon") is not None:
        unequip_weapon(character)

    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)

    character["equipped_weapon"] = item_id
    remove_item_from_inventory(character, item_id)

    return f"You equipped {item_data['name']}."


# ============================================================================
# EQUIPPING ARMOR
# ============================================================================

def equip_armor(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError("Armor not in inventory.")

    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor.")

    if character.get("equipped_armor") is not None:
        unequip_armor(character)

    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)

    character["equipped_armor"] = item_id
    remove_item_from_inventory(character, item_id)

    return f"You equipped {item_data['name']}."


# ============================================================================
# UNEQUIPPING ITEMS
# ============================================================================

def unequip_weapon(character):
    weapon_id = character.get("equipped_weapon")
    if weapon_id is None:
        return None

    # Make sure we have room
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full.")

    # Remove bonus
    return_weapon = weapon_id

    # Reverse the effect from equipped weapon
    # You must have "item_data" externally, so we store EFFECT on character
    effect = character.get("weapon_effect")
    if effect:
        stat, value = effect
        apply_stat_effect(character, stat, -value)

    character["equipped_weapon"] = None
    character["weapon_effect"] = None

    character["inventory"].append(return_weapon)
    return return_weapon


def unequip_armor(character):
    armor_id = character.get("equipped_armor")
    if armor_id is None:
        return None

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full.")

    effect = character.get("armor_effect")
    if effect:
        stat, value = effect
        apply_stat_effect(character, stat, -value)

    character["equipped_armor"] = None
    character["armor_effect"] = None

    character["inventory"].append(armor_id)
    return armor_id


# =================


