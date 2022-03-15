import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Define tcp protocol for client
client.connect(('127.0.0.1', 55556))  # Adress and port of chat server

nickname = input("Chose an nickname:")  # Ask client for nickname


def receive():  # Funktion for reciving messages form chat server
    while True:
        try:
            message = client.recv(1024).decode('utf8')
            if message == 'NICK':  # Send nickname of client when server asks for it
                client.send(nickname.encode('utf8'))
            else:
                print(message) # If not nick request print message
        except:
            print("Com error!") # If server is down disconnect ????
            client.close()
            break


def write(): # Funkstion for sending messages to chat server
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf8'))


receive_thread = threading.Thread(target=receive) # A thread for receiving messages to chat server
receive_thread.start()

write_thread = threading.Thread(target=write) # A thread for sending messages to chat server
write_thread.start()
