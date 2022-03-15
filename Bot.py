import random


def alice(a, b=None):
    return f"I think {a}ing sounds great!"


def bob(a, b=None):
    if b is None:
        return f"Not sure about {a}ing. Don't I get a choice?"
    return f"Sure, both {a} and {b}ing seems ok to me"


def dora(a, b=None):
    alternatives = ["coding", "singing", "sleeping", "fighting"]
    b = random.choice(alternatives)
    res = f"Yea, {a} is an option. Or we could do some {b}."
    return res, b


def chuck(a, b=None):
    action = a + "ing"
    bad_things = ["fighting", "bickering", "yelling", "complaining"]
    good_things = ["singing", "hugging", "playing", "working"]
    if action in bad_things:
        return f"YESS! Time for {action}"
    elif action in good_things:
        return f"What? {action} sucks. Not doing that."
    return "I don't care!"


while True:
    print("Toppics work, play, eat, cry, sleep, fight ")
    action = input("write a word with the topic")
    # action = random.choice(["work", "play", "eat", "cry", "sleep", "fight"])

    # print("\nMe: Do you guys want to {}? \n".format(action))
    print("Alice: {}".format(alice(action)))
    # print("Bob: {}".format(bob(action)))
    # print("Dora: {}".format(dora(action)[0]))
    # print("Chuck: {}".format(chuck(action)))

    if action == "_exit":
        break
