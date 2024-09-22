import random

SUCCESS_THRESHOLD = 15


def roll_dice():
    return random.randint(1, 20)  # Simulating a 20-sided dice roll


def is_successful(dice_roll, player_skill):
    return dice_roll + player_skill > SUCCESS_THRESHOLD


def determine_result(player_skill):
    dice_roll = roll_dice()
    if is_successful(dice_roll, player_skill):
        return "Success!"
    else:
        return "Failure."
