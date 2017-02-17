# assoc_laguerre expects you to make a function that creates a new function and returns it
# think of it like a factory that you can invoke to make similar functions. It's a very
# useful but also rather advanced technique

# here's an example of how it's done.

# this function is like a factory that creates specific types of functions
# these create functions all do the same thing: they take any number (as n2)
# and add a fixed number (n1) to it
# the difference between them is what this fixed number is.
def create_adder(n1):
    # let's make the adder function. A new one gets made everytime create_adder is called
    def adder(n2):
        # notice how the adder function, which gets returned, only takes n2 as a parameter
        # it already knows n1 because when it was created, n1 took on the value
        # passed into the create_adder function

        # Another way to think of it: n1 is defined when create_adder is called
        # So there's no need for adder to take in n1 as an argument. It's fixed already
        return n1 + n2

    # let's return the custom adder that we just made!
    return adder #

five_adder = create_adder(5) # returns fn that adds 5 to the number you call it with
hundred_adder = create_adder(100) # returns fn that adds 100 to the number you call it with

print five_adder(1) # prints 6
print hundred_adder(1) # prints 101
print create_adder(100)(1) # exactly the same as the above line
