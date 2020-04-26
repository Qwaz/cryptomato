from cryptomato import *


class Scheme:
    exports = [
        'n',  # param
        'MAC', 'VF'  # UF-CMA settings
    ]

    def __init__(self, n):
        # |KeySp| = 2^128
        self.prf = SecurePRF(random_bits(128), n, n)
        self.n = n
        self.visited = set()
        self.counter = 0

    @counted
    @record_dup
    def MAC(self, M):
        # CBC MAC
        # Split message into fixed-size blocks
        M = split(M, self.n)

        # IV
        cur = [0] * self.n

        for m in M:
            cur = self.prf([x ^ y for x, y in zip(m, cur)])

        return cur  # C[m]

    @counted
    @forbid_dup
    def VF(self, M, Tag):
        return self.MAC(M) == Tag


def test(module):
    # UF-CMA tester for MAC, VF
    res = [0, 0]
    counter = 0

    ITERATION = 10000
    n = 128

    for i in range(ITERATION):
        scheme = Scheme(n)
        m, tag = module.A(scheme)
        counter += scheme.counter
        res[scheme.VF(m, tag)] += 1

    failure, success = res
    adv = success / ITERATION

    return {
        "status": "success" if adv > 0.6 else "failure",
        "count": {"failure": failure, "success": success}, "average_counter": counter / ITERATION, "adv": adv
    }
