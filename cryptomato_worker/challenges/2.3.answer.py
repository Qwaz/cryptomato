# Problem 2.3
from cryptomato import *


def A(scheme):
    l = scheme.l

    z = scheme.Ek(integer_to_bits(1, l) + integer_to_bits(0, l), integer_to_bits(0, l) * 2)
    return z[l:l * 2] != z[l * 2:]
