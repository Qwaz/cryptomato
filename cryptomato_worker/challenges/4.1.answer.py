# Problem 3.3
from cryptomato import *


def A(scheme):
    h, H = scheme.h, scheme.H
    b = scheme.b
    M = [0] * b
    tag = scheme.MAC(M)
    return M + integer_to_bits(2, b), h(integer_to_bits(3, b) + tag)
