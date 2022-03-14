import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55556))

nickname = input("Chose an nickname:")

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf8')
            if message == 'NICK':
                client.send(nickname.encode('utf8'))
            else:
                print(message)
        except:
            print("Com error!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()



