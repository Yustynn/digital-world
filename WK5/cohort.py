from random import randrange

CRAPS   =   [2, 3, 12]
NATURALS =  [7, 11]

def roll_dice():
    dice = [randrange(1,7), randrange(1,7)]

    print "You rolled {} + {} = {}".format( *(dice + [sum(dice)]) )

    return sum(dice)

def lose():
    print 'You lose'
    return 0

def win():
    print 'You win'
    return 1

def play():

    roll = roll_dice()

    if roll in CRAPS:
        return lose()
    if roll in NATURALS:
        return win()

    point = roll

    while True:
        print "point is {}".format(point)
        roll = roll_dice()

        if roll == 7:
            return lose()
        if roll == point:
            return win()
        point = roll

for i in range(1):
    play()
