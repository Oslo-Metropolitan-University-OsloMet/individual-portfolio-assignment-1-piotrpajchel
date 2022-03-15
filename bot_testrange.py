import Botc

while True:
    print("Toppics work, play, eat, cry, sleep, fight ")
    action = input("write a word with the topic")
    print(f"Alice: {Botc.alice(action)}")

    if action == "_exit":
        break
