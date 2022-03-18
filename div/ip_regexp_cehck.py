
ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";

import re

#Check if the string starts with "The" and ends with "Spain":

txt = "127.0.0"
x = re.search(ValidIpAddressRegex, txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")

