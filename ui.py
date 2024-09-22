import os
import random
import sys
import pygame  # For background music
import pyttsx3
from map_bot import GameMap  # Import GameMap from map_bot.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QPushButton, QTextEdit, QProgressBar, QListWidget,
    QGraphicsView, QGraphicsScene, QLineEdit, QComboBox, QApplication, QGraphicsRectItem
)
from events import trigger_event
from npc_bot import interact_with_npc
from story_bot import get_random_intro, get_mission_story


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)  # Use PyInstaller's temp directory
    return os.path.join(os.getcwd(), relative_path)  # Use current working directory in dev


class GameWindow(QMainWindow):
    def __init__(self, character=None):
        super().__init__()
        self.character = character
        self.game_map = None
        self.current_mission_type = None

        self.initialize_voice_engine()
        self.initialize_background_music()

        # Set window properties
        self.setWindowTitle('Interactive Game with Graphical Map')
        self.setGeometry(100, 100, 1000, 700)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout()
        main_widget.setLayout(self.main_layout)

        # Top layout for character sheet and map
        top_layout = QHBoxLayout()
        self.main_layout.addLayout(top_layout)

        # Initialize the interactive window
        self.interactive_window = QTextEdit()
        self.interactive_window.setReadOnly(True)
        self.main_layout.addWidget(self.interactive_window)

        # Q's Image
        self.q_image_label = QLabel()
        self.load_q_image()
        top_layout.addWidget(self.q_image_label, 1)

        # Character sheet section
        self.character_layout = QVBoxLayout()
        self.init_character_sheet()  # Make sure this is called during initialization
        top_layout.addLayout(self.character_layout, 1)

        # Graphics View for the map
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        top_layout.addWidget(self.graphics_view, 2)

        # Command buttons layout
        self.command_button_layout = QHBoxLayout()
        self.command_buttons = []
        self.main_layout.addLayout(self.command_button_layout)

        # Initial command buttons
        self.update_command_buttons(['Create Character', 'Start Mission', 'Explore', 'Quit'])

        # Display the window
        self.show()

        # Start the introduction from Q
        self.introduce_game()

    def initialize_voice_engine(self):
        """Initialize text-to-speech engine."""
        self.voice_engine = pyttsx3.init()
        self.voice_engine.setProperty('rate', 150)
        self.voice_engine.setProperty('volume', 1)

    def initialize_background_music(self):
        """Initialize and play background music."""
        if not pygame.mixer.get_init():  # Check if mixer is already initialized
            pygame.mixer.init()
        music_path = resource_path(os.path.join("music", "Starbound Journey.mp3"))
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        else:
            print("Background music file not found at:", music_path)

    def create_character_gui(self):
        """Interface for creating a character."""
        self.character_creation_window = QWidget()
        self.character_creation_window.setWindowTitle("Create Your Character")
        self.character_creation_layout = QVBoxLayout()
        self.character_creation_window.setLayout(self.character_creation_layout)

        # Character name input
        self.name_input_label = QLabel("Enter character name:")
        self.character_creation_layout.addWidget(self.name_input_label)
        self.name_input = QLineEdit()
        self.character_creation_layout.addWidget(self.name_input)

        # Character species selection
        self.species_input_label = QLabel("Select character species:")
        self.character_creation_layout.addWidget(self.species_input_label)
        self.species_input = QComboBox()
        self.species_input.addItems(["Human", "Elf", "Dwarf", "Orc"])
        self.character_creation_layout.addWidget(self.species_input)

        # Confirm button
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_character_creation)
        self.character_creation_layout.addWidget(self.confirm_button)

        self.character_creation_window.show()

    def confirm_character_creation(self):
        """Confirm character creation and set character data."""
        name = self.name_input.text()
        species = self.species_input.currentText()
        if not name:
            self.interactive_window.append("Character name cannot be empty.")
            self.speak("Character name cannot be empty.")
            return

        # Define a basic skill set with random values
        skills = ["Strength", "Agility", "Intelligence", "Charisma", "Endurance", "Dexterity"]
        character_skills = {skill: random.randint(5, 15) for skill in skills}  # Random values between 5 and 15

        # Create the character with the generated skill set
        self.character = {
            'name': name,
            'species': species,
            'health': 100,
            'skills': character_skills,
            'items': ["Basic Sword", "Shield"]  # Add some default starting items if desired
        }

        self.initialize_character()
        self.character_creation_window.close()
        self.update_command_buttons(['Start Mission', 'Explore', 'End Mission', 'Quit'])
        self.interactive_window.append(f"Character {name} the {species} created with skills: {character_skills}!")
        self.speak(f"Character {name} the {species} has been created with a unique skill set!")

    def initialize_character(self):
        """Update character sheet details after character creation."""
        if not hasattr(self, 'character_name_label'):
            self.init_character_sheet()  # Ensure the character sheet is initialized

        self.character_name_label.setText(f"Name: {self.character['name']}")
        self.character_species_label.setText(f"Species: {self.character['species']}")
        self.health_bar.setValue(self.character['health'])

        self.skills_list.clear()
        for skill, level in self.character.get('skills', {}).items():
            self.skills_list.addItem(f"{skill}: {level}")

        self.items_list.clear()
        for item in self.character.get('items', []):
            self.items_list.addItem(item)

    def introduce_game(self):
        """Introduction from Q."""
        intro_text = get_random_intro()
        self.interactive_window.append(f"Q: {intro_text}")
        self.speak(intro_text)  # Make Q's introduction spoken

    def init_character_sheet(self):
        """Initialize character sheet display."""
        # Clear existing widgets if already initialized
        for i in reversed(range(self.character_layout.count())):
            widget = self.character_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add labels and widgets for character attributes
        self.character_name_label = QLabel("Name: -")
        self.character_species_label = QLabel("Species: -")
        self.health_bar = QProgressBar()
        self.health_bar.setMaximum(100)
        self.health_bar.setValue(0)

        # Skill and item lists
        self.skills_list = QListWidget()
        self.items_list = QListWidget()

        self.add_character_widgets()  # Add widgets to the layout

    def add_character_widgets(self):
        """Add widgets to the character sheet layout."""
        widgets = [
            self.character_name_label,
            self.character_species_label,
            QLabel("Health:"),
            self.health_bar,
            QLabel("Skills:"),
            self.skills_list,
            QLabel("Items:"),
            self.items_list
        ]

        for widget in widgets:
            self.character_layout.addWidget(widget)

    def update_command_buttons(self, commands):
        """Update the dynamic command buttons."""
        # Remove existing buttons
        for button in self.command_buttons:
            self.command_button_layout.removeWidget(button)
            button.deleteLater()
        self.command_buttons = []
        # Create and add new buttons
        for command in commands:
            btn = QPushButton(command)
            # Disable "Start Mission" and "Explore" buttons if no character exists
            if command in ["Start Mission", "Explore"] and self.character is None:
                btn.setDisabled(True)
            btn.clicked.connect(lambda _, cmd=command: self.execute_command(cmd))
            self.command_button_layout.addWidget(btn)
            self.command_buttons.append(btn)

    def execute_command(self, command):
        """Handle command execution."""
        self.interactive_window.append(f"Executing command: {command}")
        if command in ["Start Mission", "Explore"] and self.character is None:
            self.interactive_window.append("You need to create a character before starting a mission or exploring.")
            self.speak("You need to create a character before starting a mission or exploring.")  # Add voice
            return
        if command == "Create Character":
            self.create_character_gui()
            self.speak("Please create your character.")  # Voice prompt
        elif command == "Start Mission":
            self.start_mission()
            self.speak("Mission started. Good luck!")
        elif command in ["Move North", "Move South", "Move East", "Move West"]:
            self.move_player(command)
            self.speak(f"Moving {command.split()[1]}")
        elif command == "End Mission":
            self.interactive_window.append("Mission ended.")
            self.speak("Mission ended.")
            self.update_command_buttons(['Create Character', 'Start Mission', 'Explore', 'Quit'])
        elif command == "Quit":
            self.interactive_window.append("Exiting game...")
            self.speak("Exiting game.")
            self.stop_background_music()
            QApplication.quit()

    def update_character_sheet(self):
        """Update character sheet details."""
        try:
            if self.character:
                self.character_name_label.setText(f"Name: {self.character['name']}")
                self.character_species_label.setText(f"Species: {self.character['species']}")
                self.health_bar.setValue(self.character['health'])

                self.skills_list.clear()
                for skill, level in self.character.get('skills', {}).items():
                    self.skills_list.addItem(f"{skill}: {level}")

                self.items_list.clear()
                for item in self.character.get('items', []):
                    self.items_list.addItem(item)
                print("Character sheet updated successfully.")
        except Exception as e:
            print(f"Error updating character sheet: {e}")

    def load_q_image(self):
        """Load Q's image and display it in the QLabel."""
        q_image_path = resource_path(os.path.join("images", "q.jpg"))
        if os.path.exists(q_image_path):
            pixmap = QPixmap(q_image_path)
            self.q_image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.interactive_window.append("Q's image not found at the expected location.")
            print("Q's image not found at:", q_image_path)

    def speak(self, text):
        """Use text-to-speech to speak a given text."""
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()

    def start_mission(self):
        """Initialize and draw a new mission map with a storyline."""
        self.current_mission_type = random.choice(["rescue", "exploration", "stealth"])
        mission_start_story = get_mission_story(self.current_mission_type, "start")
        self.interactive_window.append(f"Mission Start: {mission_start_story}")
        self.speak(mission_start_story)  # Make the voice read out the mission start message
        # Initialize the GameMap instance
        self.game_map = GameMap(7, 7, self.current_mission_type)  # You can adjust dimensions (7x7 is used here)

        self.draw_graphical_map()
        self.update_command_buttons(['Move North', 'Move South', 'Move East', 'Move West', 'End Mission'])

    def draw_graphical_map(self):
        """Draw the map graphically in the QGraphicsView."""
        if not self.game_map:
            return

        self.graphics_scene.clear()  # Clear existing map
        tile_size = 40

        for y, row in enumerate(self.game_map.map_grid):
            for x, cell in enumerate(row):
                if cell is None:
                    continue  # Skip if the cell is None (represents an obstacle)

                rect_item = QGraphicsRectItem(x * tile_size, y * tile_size, tile_size, tile_size)

                color_map = {
                    "Start": QColor("blue"),
                    "Objective": QColor("green"),
                    "Exit": QColor("green"),
                    "Enemy": QColor("red"),
                    "Trap": QColor("black"),
                    "Treasure": QColor("yellow"),
                    "Item": QColor("orange"),
                    "Cleared": QColor("lightgray"),
                    "Empty": QColor("white"),
                    "NPC": QColor("purple")
                }

                rect_item.setBrush(QBrush(color_map.get(cell, QColor("white"))))

                if (x, y) == (self.game_map.player_x, self.game_map.player_y):
                    rect_item.setBrush(QBrush(QColor("darkmagenta")))  # Player position

                self.graphics_scene.addItem(rect_item)

        self.graphics_view.setScene(self.graphics_scene)

    def move_player(self, direction):
        """Move the player using the GameMap's logic."""
        direction_mapping = {
            "Move North": "up",
            "Move South": "down",
            "Move East": "right",
            "Move West": "left"
        }

        result = self.game_map.move_player(direction_mapping[direction])

        if result is None:
            self.interactive_window.append("You can't move in that direction.")
        else:
            self.interactive_window.append(f"You moved to a {result} room.")
            self.draw_graphical_map()
            self.check_room_encounter()

    def check_room_encounter(self):
        """Check what type of room the player has entered and handle it using trigger_event."""
        x, y = self.game_map.player_x, self.game_map.player_y
        room_type = self.game_map.map_grid[y][x]

        if room_type == "Empty":
            self.interactive_window.append("The room is empty. Nothing of interest here.")
            return

        if room_type == "NPC":
            npc_name = random.choice(["Trader", "QuestGiver"])
            dialogue = interact_with_npc(npc_name)
            self.interactive_window.append(f"{npc_name}: {dialogue}")
        else:
            if not trigger_event(room_type, self.character, self):
                self.interactive_window.append("The event failed or no further action was required.")

        if room_type in ["Enemy", "Trap", "Puzzle", "Item", "NPC"]:
            self.game_map.map_grid[y][x] = "Cleared"

        if room_type == "Objective":
            mission_end_story = get_mission_story(self.current_mission_type, "end")
            self.interactive_window.append(f"Mission Complete: {mission_end_story}")
            self.speak(f"Mission Complete: {mission_end_story}")  # Make the voice read out the mission success message
            self.update_command_buttons(['Create Character', 'Start Mission', 'Explore', 'Quit'])

    def stop_background_music(self):
        """Stop the background music."""
        pygame.mixer.music.stop()
