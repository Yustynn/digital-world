from quizF_others import sum_of_double_even_place, sum_of_odd_place, get_size
def is_valid(n):
	raw_digits = map(int, list(str(n)))
	digits = map(get_digit, [n*2 for n in raw_digits[1::2]])
	b = sum(digits)
	c = sum(raw_digits[1::2])
	print digits
	return raw_digits, digits, digits[-1::-2], b, c

	# return not (b + c) % 10


def get_digit(n):
	return n if str(n) == 1 else sum( map(int, list(str(n))) )

def prefix_matched(n, d):
	return d == get_prefix (n, len(str(d))-1 )

def get_prefix(n, k):
	return int( str(n)[0:k] )


print get_digit(2)

print get_prefix(4324324234, 3)
print get_prefix(4324324234, 1)
print get_prefix(4388576018402626,2)

print prefix_matched(4324324234, 43)
print prefix_matched(4324324234, 42)


print is_valid(4388576018410707) # T
print is_valid(4388576018402626) # F

print '4388576018410707'[-1::-2]
