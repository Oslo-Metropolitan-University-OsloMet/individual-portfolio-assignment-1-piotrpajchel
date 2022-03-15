#This is a simple server exampel using TCP

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP UDP  SOCK_DGRAM

s.bind(('127.0.0.1', 55556)) #Bind to local host
s.listen()

while True:
    client, address = s.accept()
    print("Conected to {}".format(address))
    client.send("You are conected".encode())
    client.close()