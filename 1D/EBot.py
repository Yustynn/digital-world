from eBot           import eBot
from collections    import namedtuple
from math           import acos, pi
from time           import sleep
from utils          import Line, Point

AlignmentInstruction = namedtuple('AlignmentInstruction', ['theta', 'direction'])

class EBot(eBot.eBot):
    def __init__(self, front=Point(), back=Point()):
        eBot.eBot.__init__(self) # super didn't work, was python 3?
        self.front = front
        self.back  = back
        self.connect()

    def align_to(self, target):
        direction, theta = self.get_alignment_instruction(target)
        self.pivot(direction, speed=0.2, theta=theta)

    def get_alignment_instruction(self, target):
        # dir_line = Line.from_points(self.back, self.front)
        # print dir_line.m, dir_line.c
        #
        # p = dir_line.closest_point_to(target)
        #
        # adj = self.front.dist_to(p)
        # hyp = self.front.dist_to(target)
        #
        # theta = acos(adj/hyp)

        FB = -self.front + self.back
        FT = -self.front + target

        dot = (FB.x * FT.x) + (FB.y * FT.y)
        mag_sum = FB.mag + FT.mag

        theta = acos( (dot / mag_sum) % 1 )
        print 'FB: {}, FT: {}, dot/mag_sum: {:.2f}, theta: {:.3f}'.format(FB, FT, dot/mag_sum, theta)

        z_cross = FB.x * FT.y - (FT.x * FB.y)

        if z_cross > 0:
            direction = 'counterclockwise'
        else:
            direction = 'clockwise'

        return AlignmentInstruction(direction, theta)

    def is_aligned_to(self, target):
        dir_line = Line.from_points(self.back, self.front)

        is_front_closer = self.back.dist_to(target) > self.front.dist_to(target)

        print 'is front closer: {}'.format(is_front_closer)

        print '\n\nDIRLINE CONTAINS TARGET: {}\n\n'.format(dir_line.contains(target))
        return dir_line.contains(target) and is_front_closer

    def move(self, direction='forward', speed=0.5, time=None):
        move_map = {
            'forward':  ( speed, speed),
            'backward': (-speed,-speed),
            'left':     ( 0, speed),
            'right':    ( speed, 0)
        }

        self.wheels(*move_map[direction])

        if time:
            sleep(time)
            self.stop()

    def pivot(self, direction='clockwise', speed=0.5, theta=None, time=None):
        pivot_map = {
            'clockwise':         ( speed,-speed),
            'counterclockwise':  (-speed, speed)
        }

        # if theta:
        #     init_theta = self.odometry().theta # @TODO use this

        self.wheels(*pivot_map[direction])

        if theta:
            INCR = 0.20 # experimentally obtained, loljk it's a bullshit value
            print 'Angular Movement Desired: {:.3f}, Direction: {}'.format(abs(theta), direction)
            sleep( abs(theta / INCR) * 0.1 )
            self.stop()
            return

        if time:
            sleep(time)
            self.stop()
            return

    def stop(self):
        self.wheels(0,0)
