# Problem 3.3
from cryptomato import *


def A(scheme):
    n = scheme.n
    m0, m1 = [0] * n, [1] * n
    tag1 = scheme.MAC(m0)
    tag2 = scheme.MAC(m1)
    new_tag = scheme.MAC(m0 + integer_to_bits(1, n) + tag1)
    return [1] * n + integer_to_bits(1, n) + tag2, new_tag
