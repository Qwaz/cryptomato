from Crypto import Random
from Crypto.Hash import SHA1
from Crypto.Math.Numbers import Integer
from Crypto.PublicKey import ElGamal


def sign(elg, m):
    h = int(SHA1.new(m).hexdigest(), 16)
    q = (elg.p - 1) // 2
    k = Integer.random_range(min_inclusive=1, max_exclusive=2 ** 16)
    r = pow(elg.g, k, elg.p) % q
    s = Integer(k).inverse(q) * (Integer(h) + elg.x * r) % q
    return (int(r), int(s)), int(k)


def test(module):
    m = b"Hello! Welcome to 6260 Applied Cryptography :)"

    # p = 2q + 1, both p, q is prime
    elg = ElGamal.generate(256, Random.new().read)

    (r, s), k = sign(elg, m)
    q = (elg.p - 1) // 2

    adv_x, adv_k = module.A({
        "p": int(elg.p),
        "q": int(q),
        "s": s,
        "r": r,
        "y": int(elg.y),
        "h": SHA1.new(m).hexdigest(),
        "g": int(elg.g),
        "m": m.decode()
    })

    return {"status": "success" if elg.x % q == adv_x and k == adv_k else "failure"}
