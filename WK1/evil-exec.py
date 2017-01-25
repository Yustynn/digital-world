import re
import sys

from termcolor import cprint

file = open(sys.argv[1]+'.txt')

for ln in file:
    exLetter = re.match('\((.)\)', ln).group(1)
    exCommand = re.split('\(.\) ', ln)[1]
    cprint('\n\n'+ln, 'magenta')

    try:
        exec(exCommand)
    except:
        print('Error')
