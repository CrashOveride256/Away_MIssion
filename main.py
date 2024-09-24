import os
import sys
import time
import pickle
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QSplashScreen
from ui import GameWindow  # Import the GameWindow class

# Constants for the default save file
SAVE_FILE = 'savegame.pkl'

# Function to get the correct path whether running as a packaged executable or directly from the script
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)  # Use PyInstaller's temp directory
    return os.path.join(os.getcwd(), relative_path)  # Use current working directory in dev

def load_game():
    """Load the game state from a save file."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'rb') as file:
            player_character = pickle.load(file)
            print("Game loaded successfully.")
            return player_character
    else:
        return None

def save_game(player_character):
    """Save the current game state to a file."""
    with open(SAVE_FILE, 'wb') as file:
        pickle.dump(player_character, file)
    print("Game successfully saved!")


def start_game():
    """Initialize the PyQt application, show splash screen, and load the game window."""
    app = QApplication([])  # Create the PyQt6 application instance

    # Load and show the splash screen
    splash_image_path = resource_path(os.path.join("images", "splash.jpg"))  # Ensure you have a 'splash.jpg' image
    splash_pixmap = QPixmap(splash_image_path)

    splash = QSplashScreen(splash_pixmap, Qt.WindowType.WindowStaysOnTopHint)
    splash.show()
    splash.showMessage("Loading... Please wait", alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
                       color=Qt.GlobalColor.white)

    # Process events to ensure the splash screen displays immediately
    app.processEvents()
    time.sleep(3)  # Display the splash screen for 3 seconds (adjust as needed)

    # Check if a saved game exists and ask the user what to do
    player_character = load_game()

    if player_character:
        # Ask the user if they want to load the saved game
        reply = input("A saved game was found. Do you want to load it? (y/n): ").strip().lower()

        if reply == 'y':
            game_window = GameWindow(player_character)  # Start with the loaded character
            game_window.show()
            print("Loaded saved game.")
        else:
            game_window = GameWindow(None)  # Start with no character (new game)
            game_window.show()
            print("Starting a new game.")
    else:
        game_window = GameWindow(None)  # Start with no character (new game)
        game_window.show()
        print("Starting a new game.")

    # Close the splash screen once the main window is ready
    splash.finish(game_window)

    # Start the PyQt event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    start_game()
