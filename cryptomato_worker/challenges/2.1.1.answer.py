# Problem 2.1
# Return adversary A1, A2 that breaks PRF security of scheme F1, F2


def A(scheme):
    c = scheme.F([0] * 2 * scheme.m)
    return c[:scheme.n] != c[scheme.n:]
