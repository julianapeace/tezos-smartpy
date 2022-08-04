import smartpy as sp

class AddNumber(sp.Contract):
    def __init__(self):
        self.init(42)

    @sp.entry_point
    def increment(self, quantity):
        self.data += quantity

@sp.add_test(name = "AddNumber")
def test():
    c1 = AddNumber()
    scenario = sp.test_scenario()
    scenario += c1
    scenario += c1.increment(5)
