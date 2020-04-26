from cryptomato import *


def A(scheme):
    C = scheme.Ek([0] * scheme.n * 2, [1] * scheme.n * 2)
    C = split(C, scheme.n)

    D = scheme.Dk(C[0] + [x ^ y for x, y in zip(C[1], integer_to_bits(1, scheme.n))] + C[2])
    D = split(D, scheme.n)

    # M = second block of plaintext
    M = [x ^ y for x, y in zip(D[1], integer_to_bits(1, scheme.n))]
    return M == [1] * scheme.n
