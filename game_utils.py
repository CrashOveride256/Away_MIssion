import pickle

def save_game(player_character, filename='savegame.pkl'):
    """Save the current game state to a file."""
    with open(filename, 'wb') as save_file:
        pickle.dump(player_character, save_file)
    print("Game successfully saved!")