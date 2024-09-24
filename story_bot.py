# story_bot.py
import random

# Sample lore and story elements
story_elements = {
    "intro": [
        "In a distant galaxy, you find yourself aboard a starship hurtling through space.",
        "The stars stretch out before you as you prepare for the challenges ahead.",
        "An uneasy peace has settled over the galaxy, but dangers still lurk in the shadows."
    ],
    "missions": {
        "rescue": {
            "start": "You receive a distress signal from a nearby planet. A team is stranded and needs your help.",
            "mid": "As you land, you realize the area is swarming with enemies. You must navigate carefully.",
            "end": "You successfully rescue the team and return to your ship, knowing you made a difference."
        },
        "exploration": {
            "start": "You receive orders to explore an uncharted sector of space. Unknown secrets await you.",
            "mid": "As you explore, you discover ancient ruins and strange alien technology.",
            "end": "After careful study, you uncover valuable artifacts and knowledge."
        },
        "stealth": {
            "start": "You are tasked with infiltrating an enemy base to retrieve critical data.",
            "mid": "You move through the shadows, avoiding detection from patrols and surveillance systems.",
            "end": "You retrieve the data and escape unnoticed, your mission a complete success."
        }
    }
}

def get_random_intro():
    """Return a random introduction element for the game."""
    return random.choice(story_elements["intro"])

def get_mission_story(mission_type, stage):
    """Get the story for a given mission type and stage (start, mid, end)."""
    return story_elements["missions"].get(mission_type, {}).get(stage, "Mission information is unclear...")
