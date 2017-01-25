import re
import sys

file = open(sys.argv[1]+'.txt')

for ln in file:
    exLetter = re.match('\((.)\)', ln).group(1)
    exCommand = re.split('\(.\) ', ln)[1]
    print '\n\n', exLetter, exCommand

    try:
        exec(exCommand)
    except:
        print('Error')
