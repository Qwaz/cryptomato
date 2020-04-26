import functools
import random

from Crypto.Math.Numbers import Integer


def random_bits(length):
    rand = random.getrandbits(length)
    return integer_to_bits(rand, length)


def random_int(maximum):
    # [1, l)
    return random.randrange(1, maximum - 1)


def bits_to_bytes(bits):
    assert len(bits) % 8 == 0
    return bytes([sum(b << (7 - j) for j, b in enumerate(x)) for x in split(bits, 8)])


def bits_to_integer(bits):
    return sum(b << (len(bits) - 1 - i) for i, b in enumerate(bits))


def integer_to_bits(integer, length):
    # return <integer>l
    return [(integer >> length - i - 1) & 1 for i in range(length)]


def split(bits, length):
    # Break bits into l-bit blocks: block[0] || block[1] || ...
    assert len(bits) % length == 0, "Input length must be multiple of l (%d)" % length
    return [bits[i:i + length] for i in range(0, len(bits), length)]


def merge(chunks):
    return [y for x in chunks for y in x]


def bytes_to_bits(bytes_):
    bits = [[(x >> 7 - j) & 1 for j in range(8)] for x in bytes_]
    bits = [y for x in bits for y in x]
    return bits


# Function tools

def counted(func):
    @functools.wraps(func)
    def handler(self, *args, **kwargs):
        self.counter += 1
        return func(self, *args, **kwargs)

    return handler


def record_dup(func):
    @functools.wraps(func)
    def handler(self, msg):
        res = func(self, msg)
        self.visited.add(tuple(res))
        return res

    return handler


def forbid_dup(func):
    @functools.wraps(func)
    def handler(self, msg, tag):
        assert tuple(msg) not in self.visited, "VF forbids (M, Tag)"
        return func(self, msg, tag)

    return handler


def modinv(a, p):
    return int(Integer(a).inverse(p))


class SecurePRF:
    def __init__(self, k, m, n):
        self.k, self.m, self.n = k, m, n
        self.mapping = {}
        self.inv_mapping = {}

    @staticmethod
    def gen_pair(m, src, dst, n):
        m = tuple(m)

        if m not in src:
            v = tuple(random_bits(n))
            while v in dst:
                v = tuple(random_bits(n))
            src[m] = v
            dst[v] = m
        return list(src[m])

    def __call__(self, m):
        return self.gen_pair(m, self.mapping, self.inv_mapping, self.n)

    def inv(self, c):
        return self.gen_pair(c, self.inv_mapping, self.mapping, self.m)


def _test():
    bits, bytes_ = [0, 1, 0, 1, 1, 0, 1, 1], bytes([0b01011011])

    assert bits_to_bytes(bits) == bytes_
    assert bytes_to_bits(bytes_) == bits

    assert integer_to_bits(bytes_[0], 8) == bits

    print(random_bits(8))
    print(random_int(256))
    prf = SecurePRF([1], 8, 4)
    print(prf([1] * 8))
    print(prf.inv(prf([1] * 8)))
    print(SecurePRF([1], 8, 16)([1] * 8))


if __name__ == '__main__':
    _test()
