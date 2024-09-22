# events.py

import random

from PyQt6.QtWidgets import QInputDialog

# Event data contains various encounters such as traps, enemies, puzzles, etc.
event_data = {
    "Enemy": {
        "prompt": "You encounter a hostile enemy. What do you want to do?",
        "options": ["Fight", "Flee", "Negotiate"],
        "skill": "Strength",
        "difficulty": 12,
        "success_message": "You successfully defeated the enemy!",
        "failure_message": "You were overpowered by the enemy and took damage.",
        "xp_reward": 20,
        "failure_penalty": 15
    },
    "Trap": {
        "prompt": "You triggered a trap! How do you want to handle it?",
        "options": ["Disarm", "Dodge", "Brace Yourself"],
        "skill": "Agility",
        "difficulty": 10,
        "success_message": "You deftly avoided the trap!",
        "failure_message": "The trap caught you off guard, and you suffered an injury.",
        "xp_reward": 15,
        "failure_penalty": 10
    },
    "Puzzle": {
        "prompt": "You encounter an ancient puzzle. How will you solve it?",
        "options": ["Analyze", "Guess", "Leave it alone"],
        "skill": "Intelligence",
        "difficulty": 14,
        "success_message": "You solved the puzzle and gained valuable knowledge!",
        "failure_message": "The puzzle was too complex, and you failed to solve it.",
        "xp_reward": 25,
        "failure_penalty": 5
    },
    "Item": {
        "prompt": "You find a mysterious item. What do you want to do?",
        "options": ["Take it", "Inspect it", "Leave it"],
        "skill": "Intelligence",
        "difficulty": 8,
        "success_message": "You acquired the item successfully!",
        "failure_message": "The item was trapped, and you suffered minor injuries.",
        "xp_reward": 10,
        "failure_penalty": 5
    },
    "Treasure": {
        "prompt": "You discovered a hidden treasure chest! What will you do?",
        "options": ["Open it", "Inspect it", "Leave it"],
        "skill": "Intelligence",
        "difficulty": 9,
        "success_message": "You successfully opened the treasure and found valuable items!",
        "failure_message": "The treasure was booby-trapped, and you suffered injuries.",
        "xp_reward": 20,
        "failure_penalty": 10
    }
}


def perform_skill_check(player_character, skill, difficulty):
    """
    Perform a skill check by rolling a die and adding the character's skill value.
    Returns True for success and False for failure.
    """
    # Ensure player_character['skills'] is initialized correctly
    if 'skills' not in player_character or not isinstance(player_character['skills'], dict):
        print("Error: player_character['skills'] is not initialized correctly. Initializing with default values.")
        player_character['skills'] = {"Strength": 0, "Agility": 0, "Intelligence": 0}

    skill_value = player_character['skills'].get(skill, 0)
    dice_roll = random.randint(1, 20)
    total = dice_roll + skill_value
    print(f"Skill check: Rolled {dice_roll} + {skill_value} (skill) = {total} against difficulty {difficulty}")

    return total >= difficulty


def trigger_event(room_type, player_character, game_window):
    """
    Trigger an event based on the room type and process player choices.
    """
    print(f"Triggering event for room type: {room_type}")

    # Check if the room type is "Empty" and exit early
    if room_type == "Empty":
        print("Encountered an Empty room. No event will be triggered.")
        game_window.interactive_window.append("The room is empty. Nothing of interest here.")
        return True  # Return True to indicate the encounter is complete

    # Retrieve the event data for the given room type
    event = event_data.get(room_type)
    if not event:
        print(f"No event data found for room type: {room_type}.")
        return False

    # Display the event prompt and choices to the player
    prompt = event["prompt"]
    choices = event["options"]
    player_choice, ok = QInputDialog.getItem(game_window, "Event Encounter", prompt, choices, 0, False)

    if not ok or player_choice == "Leave it alone":
        game_window.interactive_window.append("You chose to avoid the situation.")
        print("Player chose to avoid the situation.")
        return True

    print(f"Player chose: {player_choice}")

    # Handling player choices with skill checks
    if player_choice in ["Fight", "Disarm", "Analyze", "Take it", "Open it", "Inspect it"]:
        success = perform_skill_check(player_character, event["skill"], event["difficulty"])

        if success:
            try:
                # Success handling for specific event types
                if room_type == "Item" or room_type == "Treasure":
                    found_item = random.choice(["Ancient Artifact", "Healing Potion", "Mystic Amulet", "Gold Coins"])
                    print(f"Attempting to add item to inventory: {found_item}")

                    # Ensure player_character['items'] is properly initialized
                    if 'items' not in player_character or not isinstance(player_character['items'], list):
                        player_character['items'] = []

                    player_character['items'].append(found_item)

                    # Ensure XP is initialized and updated correctly
                    if 'xp' not in player_character:
                        player_character['xp'] = 0
                    player_character['xp'] += event["xp_reward"]

                    game_window.interactive_window.append(
                        f"Success! You acquired a {found_item} and gained {event['xp_reward']} XP.")

                    # Safely update character sheet
                    try:
                        game_window.update_character_sheet()
                        print("Character sheet updated successfully.")
                    except Exception as e:
                        print(f"Error updating character sheet: {e}")

                    print(f"Item acquired: {found_item}. XP awarded: {event['xp_reward']}")
                    print(f"Current Inventory: {player_character['items']}")
                    print(f"Current XP: {player_character['xp']}")
                else:
                    player_character['xp'] += event["xp_reward"]
                    game_window.interactive_window.append(event["success_message"])

                    try:
                        game_window.update_character_sheet()
                        print("Character sheet updated successfully after gaining XP.")
                    except Exception as e:
                        print(f"Error updating character sheet after gaining XP: {e}")

                    print(f"Skill check succeeded. Gained {event['xp_reward']} XP.")
            except Exception as e:
                print(f"Error while handling success outcome: {e}")
        else:
            # Failure handling for each event type
            try:
                player_character['health'] -= event["failure_penalty"]
                game_window.interactive_window.append(event["failure_message"])
                game_window.update_character_sheet()
                print(
                    f"Skill check failed. Lost {event['failure_penalty']} health. Current health: {player_character['health']}")
            except Exception as e:
                print(f"Error during failure handling: {e}")

            if player_character['health'] <= 0:
                game_window.interactive_window.append("You have died. Game over.")
                game_window.update_command_buttons(['Create Character', 'Start Mission', 'Explore', 'Quit'])
                print("Game Over: Player has died.")
                return True
        return True

    elif player_choice == "Flee":
        # Flee action handling
        game_window.interactive_window.append("You fled from the encounter, avoiding any damage.")
        print("Player fled the encounter.")
        return True

    elif player_choice == "Negotiate":
        # Handling negotiation choice
        success = perform_skill_check(player_character, "Intelligence", event["difficulty"])
        if success:
            random_reward = random.choice(["Gold", "Healing Potion", "Weapon Upgrade"])
            player_character['items'].append(random_reward)

            try:
                game_window.update_character_sheet()
                game_window.interactive_window.append(f"Negotiation succeeded! You gained a {random_reward}.")
                print(f"Negotiation succeeded. Rewarded with {random_reward}.")
            except Exception as e:
                print(f"Error updating character sheet after negotiation: {e}")
        else:
            player_character['health'] -= 5

            try:
                game_window.update_character_sheet()
                game_window.interactive_window.append("Negotiation failed, and you had to retreat. Lost 5 health.")
                print("Negotiation failed. Lost 5 health.")
            except Exception as e:
                print(f"Error updating character sheet after failed negotiation: {e}")
        return True

    return False
