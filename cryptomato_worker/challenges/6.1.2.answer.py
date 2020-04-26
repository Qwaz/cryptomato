# Problem 6.2
from cryptomato import *


def A(scheme):
    q, g, X = scheme.q, scheme.g, scheme.X
    m0, m1 = 101, 102
    Y, W = scheme.Ek(m0, m1)
    m = scheme.Dk(modinv(Y, q),
                  modinv(W, q) * pow(bits_to_integer(integer_to_bits(m0, m0.bit_length()) + scheme.H(m0)), 2, q) % q)

    return m is None
