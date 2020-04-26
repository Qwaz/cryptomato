from cryptomato import *


class Scheme:
    exports = [
        'k', 'l',  # params
        'Ek'  # IND-CPA setting
    ]

    def __init__(self, b, k, l):
        self.b, self.k, self.l = b, k, l
        self.prf = SecurePRF(random_bits(k), l, l)
        self.counter = 0

    @counted
    def Ek(self, A, B):
        assert len(A) == len(B)
        return self.E(A if self.b == 0 else B)

    def E(self, M):
        l = self.l
        M = split(M, l)
        IV = random_bits(l)
        iv = bits_to_integer(IV)

        C = [None] * (len(M) + 1)
        C[0] = IV

        for i in range(len(M)):
            C[i + 1] = self.prf(integer_to_bits(((iv + i) % 2 ** l)
                                                ^ bits_to_integer(M[i]), l))

        return merge(C)

    def D(M):
        C = split(M, l)
        iv = bits_to_integer(C[0])

        M = [None] * (len(C) - 1)

        for i in range(len(C) - 1):
            M[i] = integer_to_bits(bits_to_integer(
                prf.inv(C[i + 1])) ^ (iv + i) % 2 ** l, l)

        return merge(M)


def test(module):
    # IND-CPA tester against Ek, Dk
    ITERATION = 100
    res = [0, 0]
    counter = 0

    for i in range(ITERATION):
        k, l = 128, 128
        b = random.getrandbits(1)
        scheme = Scheme(b, k, l)
        res[module.A(scheme) == b] += 1

        counter += scheme.counter

    failure, success = res
    adv = success / ITERATION

    return {
        "status": "success" if adv > 0.6 else "",
        "count": {"failure": failure, "success": success}, "average_counter": counter / ITERATION,
        "adv": adv
    }
