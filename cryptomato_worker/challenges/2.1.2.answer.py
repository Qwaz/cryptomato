# Problem 2.1
# Return adversary A1, A2 that breaks PRF security of scheme F1, F2


def A(scheme):
    a = scheme.F([0] * scheme.m)
    b = scheme.F([1] * scheme.m)
    return [1 - i for i in a[:scheme.n]] != b[scheme.n:]
