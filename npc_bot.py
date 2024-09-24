# npc_bot.py
import random

npc_dialogues = {
    "Trader": [
        "Hello, traveler! Would you like to trade?",
        "I have valuable items for sale, if you're interested.",
        "Safe travels, friend."
    ],
    "QuestGiver": [
        "I need your help! Will you accept this mission?",
        "This task is dangerous, but you seem capable.",
        "Come back when you've completed the mission."
    ]
}

def interact_with_npc(npc_name):
    """Interact with an NPC and return their dialogue."""
    dialogue = random.choice(npc_dialogues.get(npc_name, ["The NPC remains silent."]))
    return dialogue
