import sys
import Bot

bot_type = sys.argv[2].lower()

second = sys.argv[1].lower()

if second == "bot":
    print("Ah u want a bot")
else:
    print("Yo human")

while True:
    print("Toppics work, play, eat, cry, sleep, fight ")
    action = input("write a word with the topic")

    print(Bot.response(bot_type, action))

    if action == "_exit":
        break
