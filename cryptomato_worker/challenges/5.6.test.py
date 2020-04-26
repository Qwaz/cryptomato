from Crypto.Math.Numbers import Integer
from Crypto.Util.number import getPrime, isPrime


def H(g1, g2, p, x1, x2):
    return pow(g1, x1, p) * pow(g2, x2, p) % p


def find_generator(p):
    # Just finds a group generator; not part of the challenge
    # From https://github.com/Legrandin/pycryptodome/blob/6fb4ca4c73d7e80f336c183dd8ed906d3c4320a2/lib/Crypto/PublicKey/ElGamal.py#L60
    p = Integer(p)
    while 1:
        # Choose a square residue; it will generate a cyclic group of order q.
        g = pow(Integer.random_range(min_inclusive=2,
                                     max_exclusive=p), 2, p)

        # We must avoid g=2 because of Bleichenbacher's attack described
        # in "Generating ElGamal signatures without knowning the secret key",
        # 1996
        if g in (1, 2):
            continue

        # Discard g if it divides p-1 because of the attack described
        # in Note 11.67 (iii) in HAC
        if (p - 1) % g == 0:
            continue

        # g^{-1} must not divide p-1 because of Khadir's attack
        # described in "Conditions of the generator for forging ElGamal
        # signature", 2011
        ginv = g.inverse(p)
        if (p - 1) % ginv == 0:
            continue

        # Found
        break
    return int(g)


def test(module):
    # Timeout: 1
    def verify(pairs):
        assert len(pairs) == 2 and all(len(_) == 2 for _ in pairs)
        a, b = pairs

        return H(g1, g2, p, *a) == H(g1, g2, p, *b)

    ITERATION = 8
    res = [0, 0]
    for _ in range(ITERATION):
        while True:
            p = getPrime(128)
            if isPrime((p - 1) // 2):
                break
        g1, g2 = find_generator(p), find_generator(p)
        res[verify(module.A(g1, g2, p))] += 1

    failure, success = res
    return {"status": "success" if failure == 0 else "failure", "count": {"success": success, "failure": failure}}
