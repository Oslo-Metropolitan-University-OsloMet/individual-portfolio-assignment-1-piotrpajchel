import errno
import queue
import socket
import sys
import threading

host = "127.0.0.1"  # Set server ip
port = 55556  # Set server port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Select Internet and TCP protocol
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))  # Set host ip and port
server.listen()  # Listen for incoming connections

clients = []  # List of active clients
nicknames = []  # List of nicknames for active clients

broadcast_queue = queue.Queue()


def broadcast():  # Function for sending a message from one client to all active clients

    while True:
        message = broadcast_queue.get()
        for client in clients:
            client.send(message)



    # if nick er i message ikke send den til avsender.


def handel(client):  # Function for handeling clients if client not available remove client from server
    while True:
        try:
            message = client.recv(1024)
            print(message)
            # broadcast_queue.put(message)
        except:
            print("close")
            client.close()
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast_queue.put(f'{nickname} left the chat '.encode('utf8'))
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
        broadcast_queue.put(f'{nickname} just connected'.encode('utf8'))  # Inform other chatrom users who has connected
        client.send('Connection successful, welcome to ChatyChaty !'.encode('utf8'))  # Tell client that they are
        # connected to server

        thread = threading.Thread(target=handel, args=(client,))  # Threading to be enable to handel multiple clients
        thread.start()

        print(threading.active_count())


def main():
    print("Server started")
    thread_receive = threading.Thread(target=receive)
    thread_receive.start()  # Main method start
    thread_broadcast = threading.Thread(target=broadcast)
    thread_broadcast.start()


if __name__ == "__main__":
    main()
