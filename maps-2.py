# - Step 2
# Modify the contract so that:
# - The address of the caller is used, rather than a login,
# to identify users.
# - Make users pay 5 tez for the first visit, and 3 tez for
# the next ones
# - Enforce a delay of a minimum of 10 days between two visits
# of the same user.

import smartpy as sp

owner = sp.address("tz1eGd1Gzh9cpZjW1hpzre2fLSnMAsXqRdJy")

class Visitors(sp.Contract):
    def __init__(self):
        self.init(
            visitors = {},
            wait = 10
        )

    @sp.entry_point
    def register(self, name):
        # sp.set_type(name, sp.TString)
        sp.verify(sp.amount == sp.tez(5), "User must pay 5 tez to register")
        self.data.visitors[sp.sender] = sp.record(
            visits = 0,
            name = name,
            lastLogin = sp.timestamp_from_utc_now()
        )

    @sp.entry_point
    def visit(self):
        sp.verify(sp.amount == sp.tez(3), "User must pay 3 tez to visit")
        e = self.data.visitors[sp.sender].lastLogin
        sp.verify(e.add_days(self.data.wait) - sp.timestamp_from_utc_now() < 0, "Must wait")
        self.data.visitors[sp.sender].visits += 1
        self.data.visitors[sp.sender].lastLogin = sp.timestamp_from_utc_now()

@sp.add_test(name = "Visitors")
def test():
    c1 = Visitors()
    scenario = sp.test_scenario()
    scenario += c1
    alice = sp.test_account('Alice')
    scenario += c1.register(name = "julie").run(sender = alice, amount = sp.tez(2), valid = False)
    scenario += c1.register(name = "julie").run(sender = alice, amount = sp.tez(5))
    scenario += c1.visit().run(sender = alice, amount = sp.tez(2), valid = False)
    scenario += c1.visit().run(sender = alice, amount = sp.tez(3))
    # scenario += c1.visit("chancecordelia")
    # scenario += c1.visit("chancecordelia")
