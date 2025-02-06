import random
from shutil import move
import sys
import os
import re
import copy

if __name__ == "__main__":
    filename = sys.argv[1]
  	
   # Read data from file
    with open(filename, 'r') as file:
        data = file.read()

    data = re.sub(r"\(\b(rocket|cargo|location)\b\s[rcl]\d+\)", r"", data)
   
    with open(filename, 'w') as file:
        file.write(data)