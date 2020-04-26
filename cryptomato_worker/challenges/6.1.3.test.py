def test(module):
    from Crypto.PublicKey import RSA
    ITERATION = 8
    res = [0, 0]
    for i in range(ITERATION):
        rsa = RSA.generate(1024)
        phi = (rsa.p - 1) * (rsa.q - 1)
        res[set(module.GetPQ(rsa.n, phi)) == set([rsa.p, rsa.q])] += 1

    failure, success = res

    return {"status": "success" if not failure else "failure"}
