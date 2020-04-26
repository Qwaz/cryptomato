from Crypto.Hash import SHA3_256

from cryptomato import *


class Scheme:
    exports = [
        'n', 'b',  # param
        'MAC', 'VF',  # UF-CMA settings
        'h', 'H'  # For convenience
    ]

    def __init__(self, n, b):
        # |KeySp| = 2^b
        self.K = random_bits(b)
        self.n, self.b = n, b
        self.visited = set()
        self.counter = 0

    # h: {0, 1}^(b+n) -> {0,1}^n
    @staticmethod
    def h(M):
        # SHA-3 is conjectured to be collision-resistant
        return bytes_to_bits(SHA3_256.new(b"".join(b'%d' % x for x in M)).digest())

    def H(self, M):
        M = split(M, self.b)
        m = len(M)
        v = integer_to_bits(0, self.n)
        for chunk in M:
            v = self.h(chunk + v)
        return self.h(integer_to_bits(m, self.b) + v)

    @counted
    @record_dup
    def MAC(self, M):
        return self.H(self.K + M)

    @counted
    @forbid_dup
    def VF(self, M, Tag):
        # Holds true for all deterministic schemes
        return self.MAC(M) == Tag


def test(module):
    # UF-CMA tester for MAC, VF
    res = [0, 0]
    counter = 0

    ITERATION = 100
    for i in range(ITERATION):
        n, b = 1024, 64
        scheme = Scheme(n, b)

        m, tag = module.A(scheme)
        counter += scheme.counter

        res[scheme.VF(m, tag)] += 1

    failure, success = res
    adv = success / ITERATION

    return {
        "status": "success" if adv > 0.6 else "failure",
        "count": {"failure": failure, "success": success},
        "average_counter": counter / ITERATION,
        "adv": adv
    }
