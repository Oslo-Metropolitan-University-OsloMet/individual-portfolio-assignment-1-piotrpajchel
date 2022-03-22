import socket
import threading
import time
import Bot
import sys
import logging
import argparse
import re

# ---Input validation-------------------

# Create the parser
my_parser = argparse.ArgumentParser(description='User/bot chat client for chatychaty server')

# Requierd comand line arguments for  clinet.py
my_parser.add_argument('Ip',
                       metavar='ip',
                       type=str,
                       help='Ip adress of server [0-255].[0-255].[0-255].[0-255] ')

my_parser.add_argument('Port',
                       metavar='port',
                       type=int,
                       help='Port number of server [0 - 65535]')

my_parser.add_argument('Mode',
                       metavar='mode',
                       type=str,
                       help='Two modes: user or bot | [user] or [bot]')

my_parser.add_argument('Name',
                       metavar='name',
                       type=str,
                       help='If in bot mode type bot name,Available bots: Alice, Bob, Dora, Chuck\n If in user mode '
                            'type nickname')

# Execute the parse_args() method

args = my_parser.parse_args()

# Check for valid ip format and set ip

valid_ipaddress_regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";
ip_regexp = re.search(valid_ipaddress_regex, args.Ip)

if ip_regexp:
    address = args.Ip  # server address
else:
    logging.error("Not a valid ip format, valid format: [0-255].[0-255].[0-255].[0-255] ")
    sys.exit()

# Sets port number
port = args.Port

# Check for user mode
if (args.Mode == 'user') or (args.Mode == 'bot'):
    mode = args.Mode  # user or bot mode bot
else:
    logging.error("Not valid mode, valid modes: user, bot ")
    sys.exit()

# Sets checks for vali bot name

if args.Mode == 'bot':

    bot_check = args.Name
    bot_check = bot_check.lower()
    bot_list = ['alice', 'bob', 'dora', 'chuck']

    if bot_check in bot_list:
        name = args.Name
    else:
        logging.error("Invalid bot name, valid bot names: Alice, Bob, Dora, Chuck ")

# Sets username

if args.Mode == 'user':
    name = args.Name

# ---Net code-------------------

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Define tcp protocol for client
client.connect((address, port))  # Adress and port of chat server local '127.0.0.1', 55556


# ---Bot code-------------------

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
                    bot_name = name.lower()
                    bot_reply = f'{name}: {(Bot.response(bot_name, keyword))}\n'  # Activate bot reply with keyword
                    client.send(bot_reply.encode('utf8'))
                    print(f'Bot reply: {bot_reply}')  # Console log info
                    time.sleep(0.5)  # Limit to much respons on same topic

        except:
            logging.error("Com error!")  # If server is down disconnect ´
            client.close()
            break


# ---User code------------------


def user_receive():  # Funktion for receiving messages form chat server
    while True:
        try:
            message = client.recv(1024).decode('utf8')
            if message == 'NICK':  # Send nickname of client when server asks for it
                client.send(name.encode('utf8'))
            else:
                print(f'{message}')  # If not nick request print message
                #time.sleep(0.01)  # !!!! Bufring av input uønskede mellom rom // Replase med en fifo que
        except:
            print("Com error!")  # If server is down disconnect ´
            client.close()
            break


def user_send():  # Funkstion for sending messages to chat server
    while True:
        message = f'{name}: {input("")}'
        client.send(message.encode('utf8'))


def main():
    try:
        if mode == "user":
            user_receive_thread = threading.Thread(
                target=user_receive)  # A thread for receiving messages to chat server
            user_receive_thread.start()

            user_send_thread = threading.Thread(target=user_send())  # A thread for sending messages to chat server
            user_send_thread.start()

        if mode == "bot":
            bot_io_thread = threading.Thread(target=bot_io)  # A thread for receiving messages to chat server
            bot_io_thread.start()

    except:
        logging.error("Could not start client")


if __name__ == "__main__":
    main()