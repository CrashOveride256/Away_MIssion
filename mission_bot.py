# mission_bot.py

import random
from events import perform_skill_check  # Ensure this matches the updated function in events.py

class Mission:
    def __init__(self, mission_type):
        self.mission_type = mission_type
        self.grid = self.generate_mission_grid()
        self.current_position = (0, 0)
        self.objective_position = (len(self.grid) - 1, len(self.grid[0]) - 1)
        self.completed = False

    def generate_mission_grid(self, width=5, height=5):
        """Generate a random mission grid with different encounters."""
        grid = [["Empty" for _ in range(width)] for _ in range(height)]
        grid[0][0] = "Start"
        grid[height - 1][width - 1] = "Objective"

        item_types = ["Enemy", "Trap", "Treasure", "Puzzle", "NPC"]
        for y in range(height):
            for x in range(width):
                if grid[y][x] == "Empty" and random.random() < 0.2:
                    grid[y][x] = random.choice(item_types)

        return grid

    def perform_turn(self, direction, player_character):
        """Move the player in the specified direction and handle encounters."""
        print(f"Player attempting to move {direction}")
        x, y = self.current_position

        if direction == "Move North" and y > 0:
            y -= 1
        elif direction == "Move South" and y < len(self.grid) - 1:
            y += 1
        elif direction == "Move East" and x < len(self.grid[0]) - 1:
            x += 1
        elif direction == "Move West" and x > 0:
            x -= 1
        else:
            return "Invalid move."

        self.current_position = (x, y)
        encounter = self.grid[y][x]
        print(f"Moved to position {self.current_position}, encountered {encounter}")
        encounter_result = self.handle_encounter(encounter, player_character)

        # Check if the mission is complete
        if self.current_position == self.objective_position:
            self.completed = True
            print(f"Mission objective reached at position {self.objective_position}")
            return f"Mission completed! You have reached the objective. {encounter_result}"

        return encounter_result

    def handle_encounter(self, encounter_type, player_character):
        """Handle different encounter types."""
        if encounter_type == "Enemy":
            return self.handle_combat(player_character)
        elif encounter_type == "Trap":
            return self.handle_trap(player_character)
        elif encounter_type == "Puzzle":
            return self.handle_puzzle(player_character)
        elif encounter_type == "Treasure":
            return self.handle_treasure(player_character)
        elif encounter_type == "NPC":
            return self.handle_npc_interaction(player_character)
        else:
            return "The area is empty. You continue onward."

    def handle_combat(self, player_character):
        """Handle combat encounters."""
        result = perform_skill_check(player_character, "Strength", difficulty=12)
        if result:
            player_character['xp'] += 20
            return "You defeated the enemy and gained 20 XP!"
        else:
            player_character['health'] -= 15
            return "The enemy overpowered you, and you lost 15 health."

    def handle_trap(self, player_character):
        """Handle trap encounters."""
        print(f"Handling trap encounter for player at position {self.current_position}")

        # Perform skill check
        result = perform_skill_check(player_character, "Agility", difficulty=10)

        if result:
            player_character['xp'] += 15
            print("Trap successfully disarmed. Gained 15 XP.")
            return "You avoided the trap and gained 15 XP!"
        else:
            player_character['health'] -= 10
            print(f"Trap triggered! Player health is now {player_character['health']}")

            # Check if health goes below zero
            if player_character['health'] <= 0:
                print("Player health reached 0 or below. Game over condition.")
                return "You were caught in the trap and lost 10 health! You have died."

            return "You were caught in the trap and lost 10 health."

    def handle_puzzle(self, player_character):
        """Handle puzzle encounters."""
        result = perform_skill_check(player_character, "Intelligence", difficulty=14)
        if result:
            player_character['xp'] += 25
            return "You solved the puzzle and gained 25 XP!"
        else:
            player_character['health'] -= 5
            return "The puzzle was too complex, and you lost 5 health trying to solve it."

    def handle_treasure(self, player_character):
        """Handle finding a treasure."""
        found_item = random.choice(["Healing Potion", "Energy Crystal", "Rare Artifact"])
        player_character['items'].append(found_item)
        player_character['xp'] += 10
        return f"You found a treasure containing a {found_item}! You gained 10 XP."

    def handle_npc_interaction(self, player_character):
        """Handle interaction with NPCs."""
        dialogue = random.choice([
            "The NPC offers you guidance on your mission.",
            "The NPC provides you with a healing potion.",
            "The NPC tells you about a hidden treasure nearby."
        ])
        if "healing potion" in dialogue.lower():
            player_character['items'].append("Healing Potion")
        player_character['xp'] += 10
        return f"You interacted with an NPC: {dialogue}. You gained 10 XP."

    def get_current_state(self):
        """Return the current state of the mission for display."""
        return {
            "grid": self.grid,
            "current_position": self.current_position,
            "objective_position": self.objective_position,
            "completed": self.completed
        }

def generate_mission(mission_type="exploration"):
    """Generate a new mission based on the mission type."""
    return Mission(mission_type)
