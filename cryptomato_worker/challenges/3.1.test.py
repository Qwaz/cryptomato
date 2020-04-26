from cryptomato import *


class Scheme:
    exports = [
        'k', 'n', 'l',  # params
        'Ek', 'Dk'  # IND-CCA setting
    ]

    def __init__(self, b, k, l, n):
        self.b, self.k, self.l, self.n = b, k, l, n
        self.prf = SecurePRF(random_bits(k), n, n)
        self.counter = 0
        self.visited = set()

    def SEk(self, M):
        M = split(M, self.n)
        p = len(M)

        IV = random_bits(self.n - self.l)
        L = integer_to_bits(p, self.l)

        C = [None] * (p + 1)
        C[0] = self.prf(IV + L)

        for i in range(p):
            C[i + 1] = self.prf([x ^ y for x, y in zip(C[i], M[i])])

        return merge(C)

    def SDk(self, C):
        C = split(C, self.n)
        p = len(C) - 1
        M = [None] * p

        for i in range(p):
            M[i] = [x ^ y for x, y in zip(self.prf.inv(C[i + 1]), C[i])]

        T = self.prf.inv(C[0])
        IV, p_ = T[:self.n - self.l], T[self.n - self.l:]

        return merge(M) if p_ == integer_to_bits(p, self.l) else None

    # IND-CCA common
    @counted
    def Ek(self, A, B):
        assert len(A) == len(B)
        v = self.SEk(A if self.b == 0 else B)
        self.visited.add(tuple(v))
        return v

    @counted
    def Dk(self, M):
        assert tuple(M) not in self.visited, \
            "IND-CCA: Decryption oracle forbids any ciphertext returned from encryption function"
        return self.SDk(M)


def test(module):
    # IND-CCA tester against SEk, SDk
    ITERATION = 100
    res = [0, 0]
    visited = set()

    counter = 0

    for i in range(ITERATION):
        k, l, n = 128, 32, 128
        b = random.getrandbits(1)
        scheme = Scheme(b, k, l, n)
        res[module.A(scheme) == b] += 1
        counter += scheme.counter

    failure, success = res
    adv = success / ITERATION

    return {
        "status": "success" if adv > 0.6 else "failure",
        "count": {"success": success, "failure": failure}, "average_counter": counter / ITERATION, "adv": adv
    }
