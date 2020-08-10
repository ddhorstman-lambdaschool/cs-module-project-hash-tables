# Your code here
import math
import random


def slowfun_too_slow(x, y):
    v = math.pow(x, y)
    v = math.factorial(v)
    v //= (x + y)
    v %= 982451653

    return v

powers = {}
factorials = {0: 1}

def factorial(n):
    global factorials
    if n not in factorials:
        factorials[n] = math.factorial(n)
    return factorials[n]

def power(x,y):
    global powers
    identifier = f"{x},{y}"
    if identifier not in powers:
        powers[identifier] = math.pow(x,y)
    return powers[identifier]

def slowfun(x, y):
    """
    Rewrite slowfun_too_slow() in here so that the program produces the same
    output, but completes quickly instead of taking ages to run.
    """
    v = power(x,y)
    v = factorial(v)
    v //= (x + y)
    v %= 982451653
    return v


# Do not modify below this line!
for i in range(50000):
    x = random.randrange(2, 14)
    y = random.randrange(3, 6)
    print(f'{i}: {x},{y}: {slowfun(x, y)}')
