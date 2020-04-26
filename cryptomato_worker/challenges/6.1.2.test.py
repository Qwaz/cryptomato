from Crypto.Hash import SHA3_256
from Crypto.Util.number import getPrime, isPrime

from cryptomato import *


class ElGamal:
    exports = [
        'q', 'g', 'X',  # params (including public key)
        'Ek', 'Dk',  # IND-CCA setting
        'H'  # For convenience
    ]

    def __init__(self, b, q, g):
        # ind-cca-b experiment
        self.b = b
        # ElGamal params
        self.q, self.g = q, g
        # pk, sk
        self.X, self.x = ElGamal.generate_key(q, g)
        # for report
        self.counter = 0
        self.visited = set()

    def E(self, M):
        y = random_int(self.q)
        Y = pow(self.g, y, self.q)
        K = pow(self.X, y, self.q)
        W = K * bits_to_integer(integer_to_bits(M,
                                                M.bit_length()) + ElGamal.H(M)) % self.q
        return Y, W

    def D(self, Y, W):
        K = pow(Y, self.x, self.q)
        M_ = W * modinv(K, self.q) % self.q
        M_ = integer_to_bits(M_, M_.bit_length())
        M, Z = bits_to_integer(M_[:-256]), M_[-256:]
        return Y if Z == ElGamal.H(M) else None

    @staticmethod
    def generate_key(q, g):
        x = random_int(q)
        X = pow(g, x, q)
        pk, sk = X, x
        return pk, sk

    @staticmethod
    def H(M):
        h = bytes_to_bits(SHA3_256.new(bits_to_bytes(
            integer_to_bits(M, (M.bit_length() + 7 >> 3) * 8))).digest())
        assert len(h) == 256
        return h

    # IND-CCA common
    @counted
    def Ek(self, A, B):
        v = self.E(A if self.b == 0 else B)
        self.visited.add(v)
        return v

    @counted
    def Dk(self, Y, W):
        assert (Y,
                W) not in self.visited, "IND-CCA: Decryption oracle forbids any ciphertext returned from encryption function"
        return self.D(Y, W)


def test(module):
    # IND-CCA tester against SEk, SDk
    ITERATION = 8
    res = [0, 0]
    visited = set()

    counter = 0

    for i in range(ITERATION):
        p = getPrime(512)
        b = random.getrandbits(1)
        elg = ElGamal(b, p, 2)
        res[module.A(elg) == b] += 1
        counter += elg.counter

    failure, success = res
    adv = success / ITERATION

    return {
        "status": "success" if adv > 0.6 else "failure",
        "count": {"success": success, "failure": failure}, "average_counter": counter / ITERATION, "adv": adv
    }
