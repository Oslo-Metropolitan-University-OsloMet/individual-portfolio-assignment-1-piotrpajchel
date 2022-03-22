import errno
import queue
import socket
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


def m_q():
    q_message = broadcast_queue.get()
    for client in clients:
        client.send(q_message)


def handel(client):  # Function for handeling clients if client not available remove client from server
    while True:
        try:
            message = client.recv(1024)
            # broadcast(message)
            broadcast_queue.put(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            # broadcast(f'{nickname} left the chat '.encode('utf8'))
            broadcast_queue.put(f'{nickname} left the chat '.encode('utf8'))
            nicknames.remove(nickname)
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
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of connected client is {nickname}')  # Server side system message
        # broadcast(f'{nickname} just connected'.encode('utf8'))  # Inform other chatrom users who has connected
        broadcast_queue.put(f'{nickname} just connected'.encode('utf8'))
        client.send('Connection successful, welcome to ChatyChaty !'.encode('utf8'))  # Tell client that they are

        # connected to server

        thread = threading.Thread(target=handel, args=(client,))  # Threading to be enable to handel multiple clients
        thread.start()


def main():
    print("Server started")
    thread_m_q = threading.Thread(target=m_q)  # Threading to be enable to handel multiple clients
    thread_m_q.start()
    thread_receive = threading.Thread(target=receive())
    thread_receive.start()


if __name__ == "__main__":
    main()
