import argparse
import sys
import re
import logging

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
                       help='Start s user or bot | [user] or [bot]')

my_parser.add_argument('Name',
                       metavar='name',
                       type=str,
                       help='If in bot mode type bot name,Available bots Alice, Bob, Dora, Chuck\nIf in user mode '
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

# Sets checks for valif bot name

if args.Mode == 'bot':

    bot_check = args.Name
    bot_check = bot_check.lower()
    bot_list = ['alice', 'bob', 'dora', 'chuck']

    if bot_check in bot_list:
        name = args.Name
    else:
        logging.error("Invalid bot name, valid bot names: Alice, Bob, Dora, Chuck ")
