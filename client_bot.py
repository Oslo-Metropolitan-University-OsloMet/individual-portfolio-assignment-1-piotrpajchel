import socket
import threading
import Bot

adress = ""
port = ""
mode = ""  # user bot
name = "alice"  # user name / mode

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Define tcp protocol for client
client.connect(('127.0.0.1', 55556))  # Adress and port of chat server


def bot_io():  # Funktion for reciving messages form chat server
    while True:
        try:
            message = client.recv(1024).decode('utf8')
            if message == 'NICK':  # Send nickname of client when server asks for it
                client.send(name.encode('utf8'))
            elif f"{name}:" in message: # If message from self ignore
                pass
            else:
                keyword = Bot.find_keyword(message) #Lokk for keyword in chat
                if keyword == 'None':
                    print(keyword)
                else:
                    bot_reply = f'{name}: {(Bot.response(name, keyword))}' #Reply with keyword
                    client.send(bot_reply.encode('utf8'))
        except:
            print("Com error!")  # If server is down disconnect ´
            client.close()
            break


bot_io_thread = threading.Thread(target=bot_io)  # A thread for receiving messages to chat server
bot_io_thread.start()
