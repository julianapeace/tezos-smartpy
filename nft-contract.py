# Exercise NFT.3:
# Modify this smart contract so that it can handle multiple NFTs,
# and let people mint their own NFT, providing the metadata

import smartpy as sp

owner = sp.address("tz1eGd1Gzh9cpZjW1hpzre2fLSnMAsXqRdJy")

class myNFT(sp.Contract):
    def __init__(self):
        self.init(
            nft_collection = {},
            counter = 0
        )

    @sp.entry_point
    def mint(self, color, price):
        self.data.nft_collection[self.data.counter] = sp.record(
            color = color,
            owned_by = sp.sender,
            price = price
        )
        self.data.counter += 1

    @sp.entry_point
    def transfer(self, new_owner, unique_identifier):
        sp.verify(sp.sender == self.data.nft_collection[unique_identifier].owned_by, "must be owner of NFT to transfer")
        with sp.modify_record(self.data.nft_collection[unique_identifier]) as nft:
            nft.owned_by = sp.sender

    @sp.entry_point
    def setPrice(self, new_price, unique_identifier):
        sp.verify(sp.sender == self.data.nft_collection[unique_identifier].owned_by, "must be owner of NFT to change price")
        with sp.modify_record(self.data.nft_collection[unique_identifier]) as nft:
            nft.price = new_price


    @sp.entry_point
    def buy(self, unique_identifier):
        sp.verify(sp.amount >= self.data.nft_collection[unique_identifier].price, "insufficient amount to make purchase")
        sp.send(self.data.nft_collection[unique_identifier].owned_by, sp.amount)
        with sp.modify_record(self.data.nft_collection[unique_identifier]) as nft:
            nft.owned_by = sp.sender


@sp.add_test(name = "myNFT")
def test():
    c1 = myNFT()
    alice = sp.test_account("Alice").address
    bob = sp.test_account("bob").address
    scenario = sp.test_scenario()
    scenario += c1
    # scenario += c1.mint('pink', sp.tez(7)).run(sender = owner)
    # scenario += c1.mint('blue', sp.tez(10)).run(sender = alice)

    # scenario += c1.transfer(alice).run(sender = bob, valid = False)
    # scenario += c1.transfer(alice).run(sender = owner)

    # scenario += c1.setPrice(sp.tez(10)).run(sender = owner, valid = False)
    # scenario += c1.setPrice(sp.tez(10)).run(sender = alice)

    # scenario += c1.buy().run(sender = bob, amount = sp.tez(5), valid = False)
    # scenario += c1.buy().run(sender = bob, amount = sp.tez(10))
