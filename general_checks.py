from fractions import Fraction

# N = 1, 2, ...
def is_natural_number(number):
    return isinstance(number, int) and number > 0
    
# Z = ..., -1, 0, 1, ...
def is_integer(number):
    return isinstance(number, int)

# Q = ..., -1, -1/2, 0, 1/2, 1, ...
def is_rational_number(number):
    try:
        Fraction(number)
        return True
    except (ValueError, TypeError):
        return False

