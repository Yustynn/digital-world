######### TDD SET UP ##############
GREEN = '\033[92m'
RED = '\033[91m'

def print_green(str): print GREEN + str
def print_red(str): print RED + str

def test(expr_str, expected_val):
    actual_val = eval(expr_str)

    if actual_val == expected_val:
        print_green( 'PASS! {0} == {1}'.format(expr_str, expected_val) )
    else:
        print_red( 'FAIL! Expected {0} == {1}\n{2}'.format(expr_str, expected_val,
            actual_val) )

######### HOMEWORK PROPER ##########

# PROB 1
# Solution
def cToF(temp):
    assert(temp >= -273.15) RED+"That's below absolute zero, dumbass."
    return temp * 9 / 5 + 32

# Test Cases
test("cToF(0)", 32.0)
test("cToF(-40)", -40.0)
test("cToF(100)", 212.0)


# PROB 2
# Solution
# Test Cases
test( "areaCylinder(1.0 ,2.0)", (3.141592653589793 , 6.283185307179586) )
test( "areaCylinder(2.2 ,5.0)", (15.205308443374602 , 76.02654221687301) )

# PROB 3
# Solution
# Test Cases
test( "windChillTemp(5.3 ,6)", -5.56706845588 )
test( "windChillTemp(2.2 ,4)", -6.34646224199 )

# PROB 4
# Solution
# Test Cases
test( "bmi(100 ,50)", 28.1227831856 )
test( "bmi(95.5 ,50)", 26.8572579422 )

# PROB 5
# Solution
# Test Cases
test( "investmentVal(1000 ,4.25 ,1)", 1043.34 )
test( "investmentVal (2000 ,4.25 ,3), 2271.46 )
