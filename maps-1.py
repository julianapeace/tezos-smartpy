# Exercise Maps.1
# - Step 1: add some tests

# Create a test scenario for  the visitors example contract.
# In particular, test:
# - the registration of a new user
# - multiple visits from that user
# - check that visits are counted correctly

# v = sp.local('v', 42)
# sp.if [condition]:
#     v.value += 1

# populationMap = sp.map({
#     "France": 10000000,
#     "USA": 6700000
# })
# popFrance = populationMap["France"]
# populationMap["Japan"] = 9000000

# popEurope = sp.local('popEurope', 0)
# sp.if(populationMap.contains("France")):
#     popEurope += populationMap["France"]

# del populationMap["France"] # to delete

# person = sp.record(
#     firstname = "Clare",
#     lastName = "Dupont",
#     age = 29
# )
# fullname = person.firstname + " " + person.lastname
# sp.modify_record(person, age = 32, lastname = "Mei")

import smartpy as sp

owner = sp.address("tz1eGd1Gzh9cpZjW1hpzre2fLSnMAsXqRdJy")

class Visitors(sp.Contract):
    def __init__(self):
        self.init(
            visitors = {}
        )

    @sp.entry_point
    def register(self, login, name):
        # sp.set_type(name, sp.TString)
        self.data.visitors[login] = sp.record(visits = 0, name = name)

    @sp.entry_point
    def visit(self, login):
        self.data.visitors[login].visits += 1

@sp.add_test(name = "Visitors")
def test():
    c1 = Visitors()
    scenario = sp.test_scenario()
    scenario += c1
    scenario += c1.register(login = "chancecordelia", name = "julie")
    scenario += c1.visit("chancecordelia")
    scenario += c1.visit("chancecordelia")
    scenario += c1.visit("chancecordelia")
    # start = sp.timestamp_from_utc_now()
    # scenario += c1.sub().run(sender = owner, now = start)
