from brownie import accounts, C, D


def main():
    print("Deploy contract D ...")
    d = D.deploy(1, {"from": accounts[0]})
    print(f"Contract D deployed at {d}")

    print("Deploy contract C ...")
    c = C.deploy({"from": accounts[0]})
    print(f"Contract C deployed at {c}")

    print("Call C.createD()...")
    c.createD(2, {"from": accounts[0]})

    print("Funding contract C with 3 ether")
    accounts[0].transfer(c.address, amount="3 ether")

    print("Call C.createAndEndowD()...")
    tx = c.createAndEndowD(3, "3 ether", {"from": accounts[0]})
    tx.wait(1)
    print(tx.return_value)

    print("Call C.createDSalted()...")
    tx = c.createDSalted(3, 4, {"from": accounts[0]})
    tx.wait(1)
    print(tx.return_value)
