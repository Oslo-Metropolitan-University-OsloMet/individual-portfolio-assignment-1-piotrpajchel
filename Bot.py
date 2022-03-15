import random


class Bot:

    def __init__(self, name):
        self.name = name


def find_keyword(string):
    keywords = ["work", "play", "eat", "cry", "sleep", "fight"]
    for word in string.split():
        if word in keywords:
            return word
    return "NOMATCH"


def response(bot_type, a, b=None):
    if bot_type == "alice":
        return f"I think {a}ing sounds great!"

    if bot_type == "bob":
        if b is None:
            return f"Not sure about {a}ing. Don't I get a choice?"
        return f"Sure, both {a} and {b}ing seems ok to me"

    if bot_type == "dora":
        alternatives = ["coding", "singing", "sleeping", "fighting"]
        b = random.choice(alternatives)
        res = f"Yea, {a} is an option. Or we could do some {b}."
        return res, b

    if bot_type == "dora":
        action = a + "ing"
        bad_things = ["fighting", "bickering", "yelling", "complaining"]
        good_things = ["singing", "hugging", "playing", "working"]
        if action in bad_things:
            return f"YESS! Time for {action}"
        elif action in good_things:
            return f"What? {action} sucks. Not doing that."
        return "I don't care!"
