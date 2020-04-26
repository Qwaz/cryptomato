# Problem 5.6


def A(_g1, _g2, p):
    return ((p - 1) // 2, (p - 1) // 2), (0, 0)


def H(g1, g2, p, x1, x2):
    return pow(g1, x1, p) * pow(g2, x2, p) % p
