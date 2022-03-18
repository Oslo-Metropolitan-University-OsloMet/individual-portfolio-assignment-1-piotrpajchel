
import re

while True:
    try:
        ip = "127.0.0."
        x = re.search(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
        print(x)
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")



