from math import acos, pi
from time  import sleep
from utils import Line, Point

class EBot(object):
    def __init__(self, front=Point(), back=Point()):
        self.front = front
        self.back  = back

    def angle_to(self, target):
        dir_line = Line.from_points(self.back, self.front)
        print dir_line.m, dir_line.c

        p = dir_line.closest_point_to(target)

        adj = self.front.dist_to(p)
        hyp = self.front.dist_to(target)

        theta = acos(adj/hyp)

        is_target_left_of_line = (target.x - dir_line.get_x(target.y)) > 0
        is_ebot_backward       = target.dist_to(self.back) < target.dist_to(self.front)

        if is_target_left_of_line:
            theta *= -1
        if is_ebot_backward:
            theta -= pi
            theta *= -1

        print 'is backwards: {}, is left of line: {}'.format(is_ebot_backward, is_target_left_of_line)
        print target.dist_to(self.back), target.dist_to(self.front)

        return theta

    def is_aligned(self, target):
        dir_line = Line.from_points(self.back, self.front)

        is_front_closer = self.back.dist_to(target) > self.front.dist_to(target)

        return dir_line.contains(target) and is_front_closer

    def move(self, direction='forward', movement_duration=None):
        move_map = {
            'forward':  ( 1, 1),
            'backward': (-1,-1),
            'left':     ( 0, 1),
            'right':    ( 1, 0)
        }

        self.ebot.wheels(*move_map[direction])

        if movement_duration:
            sleep(movement_duration)
            self.stop()

    def pivot(self, direction='right', movement_duration=None):
        pivot_map = {
            'left':  (-1, 1),
            'right': ( 1,-1)
        }

        self.ebot.wheels(*pivot_map[direction])

        if movement_duration:
            sleep(movement_duration)
            self.stop()

    def stop():
        self.ebot.wheels(0,0)
