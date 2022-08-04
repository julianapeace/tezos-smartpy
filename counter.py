import smartpy as sp

class Counter(sp.Contract):
    def __init__(self):
        self.init(42)

    @sp.entry_point
    def increment(self):
        self.data += 1

@sp.add_test(name = "Counter")
def test():
    c1 = Counter()
    scenario = sp.test_scenario()
    scenario += c1
    scenario += c1.increment()
