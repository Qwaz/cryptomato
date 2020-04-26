# Problem 3.2
def A(scheme):
    tag = scheme.MAC([0] * scheme.n)
    return [0] * scheme.n + tag, tag
