import random
import sys


if __name__ == '__main__':

    filename = sys.argv[1]

    lines = open(filename).readlines()
    random.shuffle(lines)
    with open(filename, 'w') as rngFile:
        rngFile.writelines(lines)
        #rngFile.write("\n")