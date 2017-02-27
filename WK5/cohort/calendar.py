lpad = lambda n: ' ' * ( 2-len(str(n)) ) + str(n)

def leap_year(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

# who am i to change Carl Gauss's notation? A is year
def day_of_week_jan1(A):
    R = lambda n, d: n % d

    return R(1 + 5*R(A-1, 4) + 4*R(A-1, 100) + 6*R(A-1, 400), 7)

def num_days_in_month(m, is_leap_year):
    return {
        1:  31,
        2:  [28, 29][is_leap_year],
        3:  31,
        4:  30,
        5:  31,
        6:  30,
        7:  31,
        8:  31,
        9:  30,
        10: 31,
        11: 30,
        12: 31
    }[m]

def first_day_of_month(m, y, is_leap_year=False):
    d_jan1 = day_of_week_jan1(y)
    days_from_jan1 = sum( map(lambda m: num_days_in_month(m, is_leap_year), xrange(1, m)) )

    return (days_from_jan1 + d_jan1) % 7

def construct_cal_month(m, d1, num_days):
    gen_wk_str = lambda start, end: ' '.join( map(lpad, xrange(start, end)) )

    month = {
        1:  'January',
        2:  'February',
        3:  'March',
        4:  'April',
        5:  'May',
        6:  'June',
        7:  'July',
        8:  'August',
        9:  'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }[m]

    result = [month]
    wk = [' ' * 3 * d1 ] # start off with initial spacing

    for day in xrange(1, num_days+1):
        entry = lpad(day)
        if (day + d1 - 1) % 7 == 0 and day > 1:
            wk = ' '.join(wk)
            result += [wk]
            wk = [' '+entry]
        else:
            wk.append(entry)

    if len(wk):
        result.append(' '.join(wk))

    return result

def construct_cal_year(y):
    d1 = lambda m: first_day_of_month(m, y, leap_year(y))
    num_days = lambda m: num_days_in_month(m, leap_year(y))

    return [y] + [construct_cal_month(m, d1(m), num_days(m)) for m in xrange(1, 13)]

def display_calendar(y, m=None):
    if m:
        d1 = first_day_of_month(m, y, leap_year(y))
        num_days = num_days_in_month(m, leap_year(y))

        data = [construct_cal_month(m, d1, num_days)]
    else:
        data = construct_cal_year(y)[1:]

    wk_header = ' ' + ' '.join(map(lpad, ['S','M','T','W','T','F','S']))

    res = ''
    for month in data:
        month[1:1] = [wk_header]
        res += wk_header + '\n'.join(month)

    return '\n\n'.join(['\n'.join(month) for month in data])
