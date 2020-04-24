import os

__all__ = (
    'TestChallenge1',
)


class TestChallenge1:
    EXPORTS = ('required_test_count', 'lr', 'guess_lr',)

    # Symmetric IND-CPA Game
    def __init__(self):
        self.attempts = 0
        self.success = 0
        self.k = None
        self.b = None

    def encrypt(self, m):
        return m[::-1]

    @staticmethod
    def required_test_count():
        return 32

    def lr(self, m0, m1):
        self.attempts += 1
        self.b = int(ord(os.urandom(1))) % 2
        if self.b == 0:
            return self.encrypt(m0)
        else:
            return self.encrypt(m1)

    def guess_lr(self, b):
        if self.b == b:
            self.success += 1
        self.b = None

    def result(self):
        if self.attempts >= 32 and self.success / self.attempts >= 0.9:
            return True, '(%d/%d)' % (self.success, self.attempts)
        return False, '(%d/%d)' % (self.success, self.attempts)
