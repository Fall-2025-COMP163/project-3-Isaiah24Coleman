"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Implementation

Name: Isaiah Coleman

AI Usage: Used Ai as well as my tutot to help me code

This module handles quest management, dependencies, and completion.
"""

import character_manager
from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    Raises: QuestNotFoundError, InsufficientLevelError,
            QuestRequirementsNotMetError, QuestAlreadyCompletedError
    """
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found.")

    quest = quest_data_dict[quest_id]

    # Check level requirement
    required_level = quest.get("required_level", 1)
    if character.get("level", 1) < required_level:
        raise InsufficientLevelError("Character level too low for this quest.")

    # Check prerequisite (if not "NONE")
    prereq = quest.get("prerequisite", "NONE")
    if prereq and prereq != "NONE":
        if prereq not in character.get("completed_quests", []):
            raise QuestRequirementsNotMetError("Prerequisite quest not completed.")

    # Check not already completed
    if quest_id in character.get("completed_quests", []):
        raise QuestAlreadyCompletedError("Quest already completed.")

    # Check not already active
    if quest_id in character.get("active_quests", []):
        raise QuestRequirementsNotMetError("Quest is already active.")

    # Add to active quests
    character.setdefault("active_quests", []).append(quest_id)
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    Raises: QuestNotFoundError, QuestNotActiveError
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found.")

    if quest_id not in character.get("active_quests", []):
        raise QuestNotActiveError("Quest is not active and cannot be completed.")

    quest = quest_data_dict[quest_id]

    # Remove from active, add to completed
    character["active_quests"].remove(quest_id)
    character.setdefault("completed_quests", []).append(quest_id)

    # Grant rewards
    xp = quest.get("reward_xp", 0)
    gold = quest.get("reward_gold", 0)

    try:
        character_manager.gain_experience(character, xp)
    except Exception:
        # If gaining XP fails for any reason, continue but do not crash here
        pass

    try:
        character_manager.add_gold(character, gold)
    except Exception:
        # If adding gold fails, continue
        pass

    return {"reward_xp": xp, "reward_gold": gold}


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    Raises: QuestNotActiveError if quest not active
    """
    if quest_id not in character.get("active_quests", []):
        raise QuestNotActiveError("Quest is not active and cannot be abandoned.")

    character["active_quests"].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    """
    active = []
    for qid in character.get("active_quests", []):
        if qid in quest_data_dict:
            active.append(quest_data_dict[qid])
    return active


def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    """
    completed = []
    for qid in character.get("completed_quests", []):
        if qid in quest_data_dict:
            completed.append(quest_data_dict[qid])
    return completed


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    Available = meets level req + prerequisite done + not completed + not active
    """
    available = []
    for qid, qdata in quest_data_dict.items():
        if can_accept_quest(character, qid, quest_data_dict):
            available.append(qdata)
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    return quest_id in character.get("completed_quests", [])


def is_quest_active(character, quest_id):
    return quest_id in character.get("active_quests", [])


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Returns True if the character meets requirements to accept quest (no exceptions)
    """
    if quest_id not in quest_data_dict:
        return False

    q = quest_data_dict[quest_id]

    # Level check
    if character.get("level", 1) < q.get("required_level", 1):
        return False

    # Already completed
    if quest_id in character.get("completed_quests", []):
        return False

    # Already active
    if quest_id in character.get("active_quests", []):
        return False

    # Prerequisite check
    prereq = q.get("prerequisite", "NONE")
    if prereq and prereq != "NONE":
        if prereq not in character.get("completed_quests", []):
            return False

    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest.
    Raises QuestNotFoundError if quest doesn't exist.
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found.")

    chain = []
    visited = set()
    current = quest_id

    while True:
        if current in visited:
            # Cycle detected; stop to avoid infinite loop
            break
        visited.add(current)

        if current not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite {current} not found.")

        chain.insert(0, current)  # build in reverse (earliest first)
        prereq = quest_data_dict[current].get("prerequisite", "NONE")
        if not prereq or prereq == "NONE":
            break
        current = prereq

    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    total = len(quest_data_dict)
    if total == 0:
        return 0.0
    completed = len(character.get("completed_quests", []))
    return (completed / total) * 100.0


def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = 0
    total_gold = 0
    for qid in character.get("completed_quests", []):
        if qid in quest_data_dict:
            q = quest_data_dict[qid]
            total_xp += q.get("reward_xp", 0)
            total_gold += q.get("reward_gold", 0)
    return {"total_xp": total_xp, "total_gold": total_gold}


def get_quests_by_level(quest_data_dict, min_level, max_level):
    result = []
    for qid, q in quest_data_dict.items():
        rl = q.get("required_level", 1)
        if rl >= min_level and rl <= max_level:
            result.append(q)
    return result

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    """
    print(f"\n=== {quest_data.get('title','(No Title)')} ===")
    print(f"ID: {quest_data.get('quest_id')}")
    print(f"Description: {quest_data.get('description')}")
    print(f"Required Level: {quest_data.get('required_level')}")
    print(f"Prerequisite: {quest_data.get('prerequisite')}")
    print(f"Rewards: {quest_data.get('reward_xp')} XP, {quest_data.get('reward_gold')} gold")


def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    """
    if not quest_list:
        print("No quests to display.")
        return

    for q in quest_list:
        print(f"- {q.get('title','(No Title)')} (Level {q.get('required_level')}) "
              f"- {q.get('reward_xp')} XP, {q.get('reward_gold')} gold")


def display_character_quest_progress(character, quest_data_dict):
    active = len(character.get("active_quests", []))
    completed = len(character.get("completed_quests", []))
    percent = get_quest_completion_percentage(character, quest_data_dict)
    totals = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n--- QUEST PROGRESS ---")
    print(f"Active quests: {active}")
    print(f"Completed quests: {completed}")
    print(f"Completion: {percent:.2f}%")
    print(f"Total XP earned: {totals['total_xp']}")
    print(f"Total Gold earned: {totals['total_gold']}")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for qid, q in quest_data_dict.items():
        prereq = q.get("prerequisite", "NONE")
        if prereq and prereq != "NONE":
            if prereq not in quest_data_dict:
                raise QuestNotFoundError(f"Prerequisite '{prereq}' for '{qid}' not found.")
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")

