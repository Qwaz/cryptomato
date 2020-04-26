from cryptomato import *


class Scheme:
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
        def _(bits):
            return [1 - x for x in bits]  # inverse

        # Problem 2.1.2
        if self.b == 1:
            return self.g(m)
        else:
            return list(self.Fbase(_(m))) + list(_(self.Fbase(m)))


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
