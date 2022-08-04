# Exercise First.3
# Create a contract that has a string as storage.
# The contract should take a string as a parameter.
# When called, it should add a comma and this parameter, at the end of the storage.
# Test this contract.

# Change the contract from the previous exercise, by adding to the Storage, the number of times that it was called.
# For example, at first, the contract may contain “Hello” and 0. Then after a call with the parameter “John”, it will contain “Hello,John” and 1. Then after another call, “Hello,John,Jennifer” and 2.
# Test this contract.

import smartpy as sp

class AddString(sp.Contract):
    def __init__(self):
        self.init(long_string = "+++begin string++", visit_counter = 0)

    @sp.entry_point
    def addString(self, value):
        self.data.long_string = self.data.long_string + ", " + value
        self.data.visit_counter += 1

@sp.add_test(name = "AddString")
def test():
    c1 = AddString()
    scenario = sp.test_scenario()
    scenario += c1
    scenario += c1.addString("add_this_string")
    scenario += c1.addString("and this")
    scenario += c1.addString("and this")
    scenario += c1.addString("and this")
    scenario += c1.addString("and this")
    scenario += c1.addString("and this")
    scenario += c1.addString("and this")
    scenario += c1.addString("and this")
    scenario += c1.addString("and this")
    scenario += c1.addString("and this")
