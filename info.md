# Away Mission Game

## Overview
**Away Mission** is an interactive, text and graphics-based RPG game where you embark on various missions, explore different environments, face challenges, and make strategic decisions. The game combines elements of turn-based role-playing with an interactive graphical map and a rich storyline. Inspired by sci-fi and fantasy themes, players encounter a variety of enemies, traps, puzzles, and NPCs as they progress through the game.

## Features
- **Graphical Map**: Explore a dynamically generated map with different room types and obstacles, visible in a grid-based layout.
- **Voice Interaction**: The game uses text-to-speech technology to read mission briefings, events, and character dialogues.
- **Character Creation**: Create your character from scratch, choosing a name and species (e.g., Human, Klingon, Vulcan, etc.), and start with a randomly generated skill set.
- **Dynamic Events**: Encounter various events such as battles, traps, puzzles, and NPC interactions as you progress through your mission.
- **Mission Objectives**: Engage in different mission types, such as rescue, exploration, and stealth, and complete objectives to succeed.

## Installation

### Prerequisites
- Python 3.8 or later
- Required Python libraries:
  - `PyQt6`
  - `pygame`
  - `pyttsx3`
  - Other dependencies included in `requirements.txt`

### Setup Instructions
1. **Clone or Download the Game Repository**:
https://github.com/CrashOveride256/Away_MIssion_full_refactor.git
2. **Install Required Packages**:
Navigate to the game directory and run: pip install -r requirements.txt
3. **Running the Game**:
- Open a terminal/command prompt in the game directory.
- Run the main game file:
  ```
  python main.py
  ```

### Building as an Executable (Optional)
You can package the game as an executable using PyInstaller:pyinstaller --onefile main.py

The executable will be located in the `dist` folder.

## Gameplay Instructions

### Starting the Game
- Upon launching, you'll be presented with a **splash screen** followed by the main menu.
- If a saved game is detected, you will be prompted to load it or start a new game.

### Creating a Character
1. Select "Create Character" from the main menu.
2. Enter a character name and choose a species.
3. The character will be initialized with a random skill set.

### Exploring the Map
- After starting a mission, you will be shown a grid-based map with different room types.
- Use the movement commands (Move North, Move South, Move East, Move West) to navigate the map.
- Encounter different events based on the room type.

### Room Types
- **Start**: Your starting position.
- **Objective**: The mission's goal – reach this room to complete the mission.
- **Enemy**: Engage in battles.
- **Trap**: Avoid or disarm traps using skill checks.
- **Treasure**: Find items and rewards.
- **Item**: Collect useful items.
- **NPC**: Interact with friendly or neutral characters.

### Mission Completion
- Complete the mission by reaching the **Objective** room and fulfilling the mission's requirements.
- You will hear mission success messages and see a summary of your journey.

## Skills and Character Progression
- Skills: Each character starts with a set of randomly generated skills (e.g., Strength, Agility, Intelligence).
- These skills determine your success in various challenges throughout the game.
- You can improve your skills as you collect items, gain experience, or interact with NPCs.

## Audio and Visuals
- **Text-to-Speech**: The game reads out mission briefings, event dialogues, and success messages.
- **Background Music**: Enjoy immersive background music that plays throughout your adventure (adjust volume or disable if needed).

## Customization
- You can replace `q.jpg` in the `images` directory to change Q's image.
- Replace `Starbound Journey.mp3` in the `music` directory to change the background music.

## Troubleshooting
- **Missing Images/Music**: Ensure that the `images` and `music` directories contain the necessary files (`q.jpg` and `Starbound Journey.mp3`).
- **PyQt6 Errors**: Make sure PyQt6 is installed correctly via `pip install pyqt6`.
- **Text-to-Speech Issues**: Ensure `pyttsx3` is properly installed, and audio drivers are working.

## Credits
- **Developer**: CrashOveride256
- **Special Thanks**: Friends and SNHU for inspiration
- **Assets**: Images and music sourced from Google.

## License
This game is licensed under the MIT License. Feel free to modify and distribute as you wish, but please provide appropriate credit.

## Contact
For support or suggestions, create an issue in the project repository.