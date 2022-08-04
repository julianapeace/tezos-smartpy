# Exercise Verifications.1
# Write a contract that stores an integer, and other information you may need.
# Anyone should be able to add to this counter, a positive value that is lower than 10.
# The same person should not be able to add twice in a row. Someone else has to call it in between.
# Note that you will need to store an address in the contract. For now, initialize it with the address of the owner of the contract. We will later see a better approach.
# Then add two entry points, one to substract a value, and one to reset the value to 0.
# Only the owner of the contract may call these entry points.

# sp.source is the address who signed and send the operation,
# sp.sender is the address of the current caller
# sp.self_address is the address of the SC itself

import smartpy as sp

owner = sp.address("tz1eGd1Gzh9cpZjW1hpzre2fLSnMAsXqRdJy")
alice = sp.test_account("Alice")
bob = sp.test_account("Bob")

class Verifications(sp.Contract):
    def __init__(self):
        self.init(value = 0, lastSender = owner)

    @sp.entry_point
    def add(self, value):
        sp.verify(value > 0, "Value must be positive")
        sp.verify(value < 10, "Value must be less than 10")
        sp.verify(self.data.lastSender != sp.source, "The same person should not be able to add twice in a row.")
        self.data.value += value
        self.data.lastSender = sp.source

    @sp.entry_point
    def substract(self, value):
        sp.verify(sp.sender == owner, "Only the owner may substract")
        self.data.value -= value

    @sp.entry_point
    def reset(self):
        sp.verify(sp.sender == owner, "Only the owner may reset")
        self.data.value = 0

@sp.add_test(name = "Verifications")
def test():
    c1 = Verifications()
    scenario = sp.test_scenario()
    scenario += c1
    scenario += c1.add(3).run(sender = alice)
    scenario += c1.add(1).run(sender = alice) #should error out
    scenario += c1.substract(2).run(sender = owner)
    scenario += c1.reset().run(sender = owner)
