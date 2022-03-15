import socket
import threading

# 'ascii' to 'utf8'

host = "127.0.0.1"  # Set server ip
port = 55556  # Set server port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Select Internet and TCP protocol
server.bind((host, port))  # Set host ip and port
server.listen()  # Listen for incoming connections

clients = []  # List of active clients
nicknames = []  # List of nicknames for active clients


def broadcast(message):  # Function for sending a message from one client to all active clients
    for client in clients:
        client.send(message)


def handel(client):  # Function for handeling clients if client not available remove client from server
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat '.encode('utf8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, adress = server.accept()  # Looking for conection
        print(f'Conected with {str(adress)}')  # Server side system message

        client.send('NICK'.encode('utf8'))  # Asking for nickname from client
        nickname = client.recv(1024).decode('utf8')  # Receive nickname and store nickname and client in lists
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of connected client is {nickname}')  # Server side system message
        broadcast(f'{nickname} just connected'.encode('utf8'))  # Inform other chatrom users who has connected
        client.send('Connection successful, welcome to ChatyChaty !'.encode('utf8'))  # Tell client that they are
        # connected to server

        thread = threading.Thread(target=handel, args=(client,))  # Threading to be enable to handel multiple clients
        thread.start()


print("Server started")
receive()  # Main method start
