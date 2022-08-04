# Exercise Transactions.2
# Change the  deposit entry point so that allows anyone to deposit
# at least 100 tez. When doing so, the caller may change the withdrawal
# limit. The caller may not reduce the withdrawal limit below 1 though.

import smartpy as sp

owner = sp.address("tz1eGd1Gzh9cpZjW1hpzre2fLSnMAsXqRdJy")

class Collect(sp.Contract):
    def __init__(self):
        self.init(
            lastCallTime = sp.timestamp_from_utc_now(),
            max = sp.tez(100),
            wait = 10
        )

    @sp.entry_point
    def collect(self, amount):
        sp.verify(sp.sender == owner, "must be owner")
        sp.verify(amount > self.data.max, "must not overdraw")
        sp.verify(sp.now - self.data.lastCallTime < self.data.wait, "Please wait a little longer")
        sp.send(owner, amount)
        self.data.lastCallTime = sp.now

    @sp.entry_point
    def donate(self, newMax):
        message = sp.pair("not enough tez", self.data.max)
        sp.verify(sp.amount > self.data.max, message)
        sp.if newMax != sp.none:
            sp.verify(newMax.open_some() > sp.tez(1), "Cannot reduce max to below 1")
            sp.verify(newMax.open_some() < self.data.max, "New max is too high")
            self.data.max = newMax.open_some()
        pass

@sp.add_test(name = "Collect")
def test():
    c1 = Collect()
    alice = sp.test_account("Alice").address
    bob = sp.test_account("Bob").address
    scenario = sp.test_scenario()
    scenario += c1

    start = sp.timestamp_from_utc_now()
    # Donates 130 to contract
    scenario += c1.donate(sp.none).run(sender = alice, amount = sp.tez(130))
    # Donates too little. Should fail.
    scenario += c1.donate(sp.none).run(sender = alice, amount = sp.tez(30), valid = False)
    # Donates enough to update the newMax to 50
    scenario += c1.donate(sp.some(sp.tez(50))).run(sender = alice, amount = sp.tez(130))
    # Donates enough to update new Max. But new Max is too high. Should fail.
    scenario += c1.donate(sp.some(sp.tez(120))).run(sender = alice, amount = sp.tez(130), valid = False)
    # Owner withdraws 99 tez
    scenario += c1.collect(sp.tez(99)).run(sender = owner)
    # Owner over withdraws 1000 tez. Should fail.
    scenario += c1.collect(sp.tez(1000)).run(sender = owner, valid = False)




# sp.verify(sp.utils.nat_to_tez(newMax) < sp.utils.tez_to_nat(self.data.max), "new maximum limit is too low")
