# q_responses.py
import random

# Constants for default responses and Q responses
DEFAULT_RESPONSES = [
    "Oh, is that the best you can do? Try asking something more interesting next time.",
    "You really ought to be more creative. I expect better questions from you.",
    "Honestly, I thought you'd be more entertaining. Try again."
]

Q_RESPONSES = {
    "who am i": [
        "Oh, you again. You're just an insignificant speck in this vast universe, but for now, you’re an Ensign. Consider yourself lucky.",
        "Why do you even bother asking? You're just another Ensign trying to prove yourself. But don't worry, I'll keep you entertained."
    ],
    "what's my mission": [
        "Your mission? As if you actually have one! You're here to survive my little game, and maybe learn a thing or two about this 'Starfleet' you adore.",
        "You want a mission? Fine. How about not getting yourself vaporized in the first five minutes? That’s a start."
    ],
    "where am i": [
        "You’re on a starship, lost in the vastness of space. But let's be honest, you're lost in more ways than one, aren't you?",
        "Aboard your ship, but trust me, your location doesn’t matter. What matters is what you do now, which, knowing you, probably isn’t much."
    ],
    "what is happening": [
        "Oh, you poor thing. You’re caught in one of my delightful little games! Pay attention, and maybe you’ll live to see another star.",
        "Something beyond your comprehension, I assure you. But don't worry, I'll dumb it down for you as we go along."
    ],
    "help": [
        "Help? Really? This is Starfleet; you're supposed to be able to handle yourself. But fine, I might throw you a bone, if I feel like it.",
        "You want help? How quaint. I’ll consider it… but don’t expect me to be your personal guide every step of the way.",
        "You're looking for help, are you? How disappointing. But fine, check the area around you, sometimes the simplest path is the right one.",
        "If I were you, I'd take another look at that control panel. It might be more important than you think.",
        "Why not try using that communicator of yours? You might find an answer by calling for assistance.",
        "You could always use your phaser on the obstacle. Just make sure it's set to stun."
    ],
    "advice": [
        "Advice? From me? Ha! Alright, here’s a nugget of wisdom: Don’t get yourself killed. It’s such a waste of my time.",
        "If you insist on advice, how about this: Try not to embarrass yourself more than usual. I have high standards, you know.",
        "Advice? Don’t get yourself killed, for starters. And keep an eye on your surroundings, they might hold the key to success.",
        "If you must insist on surviving, remember: Phaser combat is more effective when you aim for weak points.",
        "Stay alert. The real danger often lies in what you can’t see."
    ],
    "challenge": [
        "Oh, you want a challenge, do you? Very well. Find a way to make peace with a Klingon without using your phaser. Good luck with that!",
        "A challenge? Fine. Figure out how to bypass a Borg cube’s defenses without getting assimilated. I’ll wait."
    ],
    "starfleet": [
        "Starfleet… Oh, where do I begin? An organization of idealists prancing about the galaxy, pretending they’re making a difference.",
        "Starfleet, the so-called beacon of hope. In reality, it’s just a bunch of humans trying to play hero in a universe that barely notices them."
    ],
    "humans": [
        "Humans... so predictable, so fragile, and yet you keep surprising me. You're like a cosmic joke that never gets old.",
        "Humans are fascinating in a 'watching-a-train-wreck' kind of way. I mean, you make the same mistakes over and over again. It’s endearing, really."
    ]
}


def get_response(question):
    """Retrieve a response from Q based on the player's question."""
    question_key = _sanitize_question(question)
    return _get_random_response(Q_RESPONSES, question_key, DEFAULT_RESPONSES)


def _sanitize_question(question):
    """Sanitize and standardize the user's question."""
    return question.lower().strip()


def _get_random_response(responses_dict, question, default_responses):
    """Retrieve a random response based on the given question."""
    return random.choice(responses_dict.get(question, default_responses))
