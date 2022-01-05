from web3 import Web3
from solcx import compile_source
from Solidity_code import *

compiled_sol = compile_source(
    solidity_code, output_values=["abi", "bin"])

contract_id, contract_interface = compiled_sol.popitem()

# Access to abi and bytecode
bytecode = contract_interface['bin']
abi = contract_interface['abi']

# connect to Rinkeby
w3 = Web3(Web3.HTTPProvider(
    "https://rinkeby.infura.io/v3/1ee4a6adc6584fbeaa8c7cea3b8dbbc5"))
contract_ = w3.eth.contract(abi=abi, bytecode=bytecode)

# connect to Account
acct = w3.eth.account.privateKeyToAccount(
    '086a4b3fe152bfff7c2442577cedd9a8e60841282cded459d7de8d8f6f234d35')


# transaction to deploy contract
construct_txn = contract_.constructor().buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})

signed = acct.signTransaction(construct_txn)

final = w3.eth.sendRawTransaction(signed.rawTransaction)

# print smart contract address
flag = 0
while flag == 0:

    try:
        flag = 1
        print(w3.eth.getTransactionReceipt(final.hex())["contractAddress"])
    except:
        flag = 0
