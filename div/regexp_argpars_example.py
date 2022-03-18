import argparse
import re
from uuid import uuid4

def my_regex_type(arg_value, pat=re.compile(r"^[a-f0-9A-F]{32}$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

parser = argparse.ArgumentParser()
parser.add_argument('hex', type=my_regex_type)

args = parser.parse_args([uuid4().hex])