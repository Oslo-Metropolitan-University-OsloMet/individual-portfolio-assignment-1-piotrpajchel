import socket
import threading
import Bot
import sys

address = sys.argv[1]  # server address
port = int(sys.argv[2])  # server port
mode = sys.argv[3]  # user or bot mode bot
name = sys.argv[4]  # user name / mode

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Define tcp protocol for client
client.connect((address, port))  # Adress and port of chat server local '127.0.0.1', 55556


def bot_io():  # Funktion for reciving messages form chat server
    while True:
        try:
            message = client.recv(1024).decode('utf8')
            if message == 'NICK':  # Send nickname of client when server asks for it
                client.send(name.encode('utf8'))
                print(f'Bot: {name} connected')  # Console log info
            elif f"{name}:" in message:  # If message from self ignore to avoid feedback
                pass
            else:
                keyword = Bot.find_keyword(message)  # Check i chat message has a reply keyword
                if keyword != "NOMATCH":  # Keword is a match
                    bot_reply = f'{name}: {(Bot.response(name, keyword))}'  # Activate bot reply with keyword
                    client.send(bot_reply.encode('utf8'))
                    print(f'Bot reply: {bot_reply}')  # Console log info

        except:
            print("Com error!")  # If server is down disconnect ´
            client.close()
            break


bot_io_thread = threading.Thread(target=bot_io)  # A thread for receiving messages to chat server
bot_io_thread.start()
