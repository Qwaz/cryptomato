# Problem 6.3


def GetPQ(N, phi):
    def sqrt(x):
        from Crypto.Math.Numbers import Integer
        return int(Integer(x).sqrt())

    x = -phi + N + 1
    y = sqrt(x ** 2 - 4 * N)
    return (x + y) // 2, (x - y) // 2
