def is_timings_conflict(timings):
    for i in range( len(timings) ):
        # timings.pop() removes the last element from timings and gives it to us
        # start and end become the 0th and 1st elements of the removed tuple
        start, end = timings.pop()

        for comp_timing in timings: # timings now has 1 less element!
            comp_start, comp_end = comp_timing
            # below brackets just to see clearer. A little convoluted...
            # if it doesn't start after the comp_end, or end before the comp_start...
            if not ( (end <= comp_start ) or (start >= comp_end) ):
                return True

    return False

# Note that the profs got the naming convention
# for Python wrong. Should be find_conflict, not findConflict. They fixed it
# starting this year.
def findConflict(sched):
    conflict_store = {}

    for day, timings in sched.items():
        conflict_store[day] = is_timings_conflict(timings)

    return conflict_store


def getSchedule(f):
    sched = {}
    timings = []

    for line in f:
        val = line.split() # either day or timing

        if len(val) == 1: # if only 1 element, it's gotta be the day
            day = val[0]
            timings = [] # reset day_timings to new list for new day's timings
            sched[day] = timings
        else: # else, it's a timing
            timing = map(int, val) # turns timing into integers from strings
            timings.append( tuple(timing) ) # add to current list for current day

    return sched


def findLength(sched):
    length = {}

    for day, timings in sched.items():
        hours_count = 0

        for timing in timings:
            hours_count += timing[1] - timing[0]

        length[day] = hours_count

    return length

sched = {'Tuesday': [(12, 16), (9, 12), (15, 18), (19, 21)], 'Thursday': [(7, 11), (10, 13)], 'Wednesday': [(6, 8)], 'Monday': [(9, 11), (12, 14), (11, 12)]}

print findLength(sched)
