from cryptomato import *


class Scheme:
    """
    PRF: k-bits x m-bits => n-bits
    """
    exports = [
        'k', 'm', 'n',  # params
        'F'  # PRF setting
    ]

    def __init__(self, b, k, m, n):
        self.b = b
        self.k, self.m, self.n = k, m, n
        self.Fbase = SecurePRF(random_bits(k), m, n)
        self.g = SecurePRF(random_bits(k), m, n)
        self.counter = 0

    @counted
    def F(self, m):
        assert self.b in (0, 1)

        if self.b == 1:
            return self.g(m)
        else:
            # Problem 2.1.1
            assert len(m) % 2 == 0
            mid = len(m) // 2
            return self.Fbase(m[:mid]) + self.Fbase(m[mid:])


def test(module):
    # PRF tester
    counter = [0]
    ITERATION = 100

    res = [0, 0]

    for i in range(ITERATION):
        k, m, n = 64, 64, 64
        b = random.getrandbits(1)
        scheme = Scheme(b, k, m, n)
        res[module.A(scheme) == b] += 1

    failure, success = res
    adv = success / ITERATION

    return {
        "status": "success" if adv > 0.6 else failure,
        "count": {
            "failure": failure,
            "success": success
        },
        "average_counter": counter[0] / ITERATION,
        "iteration": ITERATION,
        "adv": adv
    }
