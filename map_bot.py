import random
from PyQt6.QtWidgets import QInputDialog  # Import QInputDialog for GUI input handling
from events import perform_skill_check  # Update the import statement to use perform_skill_check
from mission_bot import generate_mission  # Import the mission generator

class GameMap:
    def __init__(self, width, height, mission_type):
        self.width = width
        self.height = height
        self.mission_type = mission_type
        self.map_grid = [[None for _ in range(width)] for _ in range(height)]
        self.player_x = 0
        self.player_y = 0
        self.objective_x, self.objective_y = self.place_objective()
        self.populate_map()

    def place_objective(self):
        """Randomly place the main mission objective."""
        return random.randint(0, self.width - 1), random.randint(0, self.height - 1)

    def populate_map(self):
        room_types = ["Empty", "Enemy", "Trap", "Puzzle", "Item"]
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == (self.objective_x, self.objective_y):
                    self.map_grid[y][x] = "Objective"
                else:
                    self.map_grid[y][x] = random.choice(room_types)

        # Ensure the start and exit points are defined
        self.map_grid[0][0] = "Start"
        self.map_grid[self.height - 1][self.width - 1] = "Exit"

    def display_map(self):
        for row in self.map_grid:
            print(" | ".join(row))

    def move_player(self, direction):
        """Move the player in the specified direction."""
        if direction == "up" and self.player_y > 0:
            self.player_y -= 1
        elif direction == "down" and self.player_y < self.height - 1:
            self.player_y += 1
        elif direction == "left" and self.player_x > 0:
            self.player_x -= 1
        elif direction == "right" and self.player_x < self.width - 1:
            self.player_x += 1
        else:
            print("You can't move in that direction.")
            return None

        current_room = self.map_grid[self.player_y][self.player_x]
        print(f"You moved to a {current_room} room.")
        return current_room

    def is_objective_reached(self):
        return self.player_x == self.objective_x and self.player_y == self.objective_y

# Example usage of map_bot.py
def start_mission(player_character, mission_type, game_window):
    game_map = GameMap(5, 5, mission_type)  # Create a 5x5 grid with the given mission type
    mission = generate_mission(mission_type)  # Generate the mission using mission_bot
    game_window.update_map_display(game_map)  # Display the initial map

    while not mission.completed:
        direction, ok = QInputDialog.getText(game_window, "Movement",
                                             "Enter direction (up, down, left, right) or 'quit':")
        if not ok or not direction:
            continue

        direction = direction.strip().lower()

        if direction == "quit":
            game_window.interactive_window.append("You have abandoned the mission.")
            break

        result = game_map.move_player(direction)

        if result == "invalid_move":
            game_window.interactive_window.append("You can't move in that direction.")
        else:
            game_window.update_map_display(game_map)  # Update map display
            game_window.interactive_window.append(f"You moved to a {result} room.")
            mission.perform_turn(game_map, player_character)

        if mission.completed:
            game_window.interactive_window.append("Mission complete!")
            break
