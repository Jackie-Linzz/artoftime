

tables = {}
waiting = {}

class waitingStatus(object):
    def __init__(self):
        self.keep = []
        self.low = -1
        self.high = -1

    def add(self):
        if (self.high + 1) % 100 == self.low:
            return "sorry"
        self.high += 1
        self.keep.append(self.high)
        if len(self.keep) == 1:
            self.low = self.high
        return self.high

    def remove(self, t):
        if t not in self.keep:
            return "sorry"
        self.keep.remove(t)
        if len(self.keep) == 0:
            self.low = -1
            self.high = -1
            return
        if t == self.low:
            while self.low not in self.keep:
                self.low = (self.low + 1) % 100
            return

    def length(self):
        return len(self.keep)


ws = waitingStatus()

