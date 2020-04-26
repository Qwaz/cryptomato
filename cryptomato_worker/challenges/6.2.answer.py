#!/usr/bin/python3

from Crypto.Math.Numbers import Integer


def A(params):
    p, q, s, r = params['p'], params['q'], params['s'], params['r']
    y, h, g, m = params['y'], params['h'], params['g'], params['m']

    h = int(h, 16)

    for k in range(1, 2 ** 16):
        if pow(g, k, p) % q == r:
            recovered_k = k
            break

    k = Integer(recovered_k)
    # s <- k^-1(h + xr) mod q
    # Then x = r^-1(ks - h)
    x = Integer(Integer(s) * k % q - h) * Integer(r).inverse(q) % q
    assert s == k.inverse(q) * (Integer(h) + x * r) % q

    return (x + ((p - 1) // 2) * 0) % p, k
