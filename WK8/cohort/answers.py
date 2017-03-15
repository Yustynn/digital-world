# QUESTION 3

from time import time, sleep

class StopWatch():
    def __init__(self):
        self.start()
        
    def start(self):
        self.start_time, self.end_time = time(), -1

    def stop(self):
        self.end_time = time()

    def elapsed_time(self):
        elapsed = round(self.end_time - self.start_time, 1)

        if elapsed >= 0:
            return elapsed
    
sw = StopWatch()
sleep(0.1)
sw.stop()
print sw.elapsed_time()
sw.start()
sleep(0.2)
print sw.elapsed_time()
sw.stop()
print sw.elapsed_time()


# QUESTION 4

class Line():
    def __init__(self, c0, c1):
        self.c0, self.c1 = c0, c1

    def __call__(self, x):
        return self.c0 + x*self.c1

    def table(self, start, end, n):
        stringify = lambda n: '%0.2f' % n

        x = start = float(start)
        step = (end - start) / (n-1)

        while x <= end:
            y = self(x)

            str_x, str_y = map(stringify, [x,y])
            num_spaces = 10 - sum( map(len, [str_x,str_y]) )
            spaces = ' ' * num_spaces
            print str_x + spaces + str_y
            x += step

