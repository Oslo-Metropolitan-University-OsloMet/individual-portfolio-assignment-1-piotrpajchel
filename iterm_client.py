#This is a simple client exampel using TCP

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP UDP  SOCK_DGRAM
s.connect(('127.0.0.1', 55556))
message = s.recv(1024)
s.close()


print(message.decode())