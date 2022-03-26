import queue
import socket
import threading
import time

host = "127.0.0.1"  # Set server ip
port = 55556  # Set server port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Select Internet and TCP protocol
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Make server address reusable
server.bind((host, port))  # Set host ip and port
server.listen()  # Listen for incoming connections

clients = []  # List of active clients
nicknames = []  # List of nicknames for active clients

broadcast_queue = queue.Queue()


def cli():
    while True:

        cli_in = input(">>")

        if cli_in == "-help":
            print(f'Valid CLI commands:\n'
                  f'<list> List all activ users\n'
                  f'<kick> Remove user from server\n'
                  f'<-help> or <man> Display help information')

        elif cli_in == "list":
            print("List of connected clients: ")
            for nickname in nicknames:
                print(nickname)

        elif cli_in == "kick":
            kick = input("Enter name of client to kick:")
            for n in nicknames:
                if n == kick:
                    index = nicknames.index(kick)
                    client = clients[index]
                    client.send('KICK'.encode('utf8'))
        else:
            print(f'{cli_in} not a valid input command ')


def broadcast_q():  # Function for sending a message from one client to all active clients

    while True:
        message = broadcast_queue.get()

        try:
            # Gets first string in message and finds name tag

            name_tag = message.decode('utf8').split()[0].replace(":", "")

            sender_index = nicknames.index(name_tag)  # Finds index of sender

            # Makes sender_list that sends to every one exept sender

            send_list = [element for i, element in enumerate(clients) if i not in {sender_index}]

            for client in send_list:
                client.send(message)
                time.sleep(0.001)
        except:
            print("Sender not in list")

            # Sending disconect message to everyone

            for client in clients:
                client.send(message)
                time.sleep(0.001)







def handel(client):  # Function for handling clients if client not available remove client from server


    while True:

        message = client.recv(1024)

        if message:  # if message is not zero byte and not kicked
            broadcast_queue.put(message)
        else:  # when client disconnects zero byte stream is send / Disconnect client and end stop thread
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast_queue.put(f'{nickname} left the chat '.encode('utf8'))
            nicknames.remove(nickname)
            print(f'client removed {nickname}')
            break


def set_keepalive(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds

    https://www.programcreek.com/python/example/4925/socket.SO_KEEPALIVE example 17
    """
    if hasattr(socket, "SO_KEEPALIVE"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    if hasattr(socket, "TCP_KEEPIDLE"):
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    if hasattr(socket, "TCP_KEEPINTVL"):
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    if hasattr(socket, "TCP_KEEPCNT"):
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


def receive():
    while True:
        client, adress = server.accept()  # Looking for conection
        print(f'Conected with {str(adress)}')  # Server side system message
        set_keepalive(client)  # Keep TCP konection alive to
        client.send('NICK'.encode('utf8'))  # Asking for nickname from client
        nickname = client.recv(1024).decode('utf8')  # Receive nickname and store nickname and client in lists
        if nickname in nicknames:
            print(f"{nickname} already in use")
            client.send('NICK_INVALID'.encode('utf8'))
        else:
            client.send('NICK_OK'.encode('utf8'))
            nicknames.append(nickname)
            clients.append(client)
            print(f'Nickname of connected client is {nickname}')  # Server side system message
            broadcast_queue.put(f'{nickname} just connected'.encode('utf8'))  # Broadcast new user conection
            client.send(
                'Connection successful, welcome to ChatyChaty !'.encode('utf8'))  # Tell user client that they are
            # connected to server

            # Threading to be enabled to handel multiple clients
            thread = threading.Thread(target=handel, args=(client,))
            thread.start()

            print(f'Thread count:{threading.active_count()}')


def main():
    print("Server started")
    thread_receive = threading.Thread(target=receive)
    thread_receive.start()  # Main method start
    thread_broadcast_q = threading.Thread(target=broadcast_q)
    thread_broadcast_q.start()
    thread_cli = threading.Thread(target=cli)
    thread_cli.start()


if __name__ == "__main__":
    main()
