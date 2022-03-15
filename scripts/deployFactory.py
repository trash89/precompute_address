from brownie import accounts, Factory, FactoryAssembly, TestContract


def main():
    print("Deploy TestContract...")
    tc = TestContract.deploy(accounts[1].address, 123, {"from": accounts[0]})
    print(f"Deployed at {tc}...")

    print("Deploy Factory...")
    f = Factory.deploy({"from": accounts[0]})
    print(f"Deployed at {f}...")

    print("Call Factory.deploy()...")
    tx = f.deploy(accounts[2].address, 123, 456, {"from": accounts[0]})
    tx.wait(1)
    print(f"A new TestContract was created at address {tx.return_value}")

    print("Deploy FactoryAssembly...")
    fa = FactoryAssembly.deploy({"from": accounts[0]})
    print(f"Deployed at {fa}...")

    print("Call FactoryAssembly.getBytecode..")
    bytecodeTC = fa.getBytecode(tc.address, 123)

    print("Call FactoryAssembly.getAddress..")
    newSalt = 789
    new_address = fa.getAddress(bytecodeTC, newSalt)
    print(f"The new TestContract will be created at {new_address}")

    print("Create the new TestContract")
    tx = fa.deploy(bytecodeTC, newSalt, {"from": accounts[0]})
    tx.wait(1)
    print(f"New contract created at {tx.new_contracts}")
