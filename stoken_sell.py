import os
import time
from random import randint

from dotenv import load_dotenv
from web3 import Web3

from data import bnb_token_address, panabi, panRouterContractAddress, sellAbi

#  Contract Address of Token we want to buy Какой токен продаем
sell_token = '0xe9e7cea3dedca5984780bafc599bd69add087d56'

#  Случайным образом выбираем кошелек с которого продаем
random_wallet = randint(1, 1)
print(f'Number wallet: {random_wallet}')

bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

load_dotenv()

wallet = os.getenv('WALLET_' + str(random_wallet)).split('||')

wallet_address = str(wallet[0])
private_key = str(wallet[1])

spend = web3.toChecksumAddress(bnb_token_address)

# Setup the PancakeSwap contract
contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)

#  извлекаем и печатаем балланс кошелька BNB
balance = web3.eth.get_balance(wallet_address)
humanReadable = web3.fromWei(balance, 'ether')
print(f'Your ballance:  {humanReadable} BNB')

tokenToSell = web3.toChecksumAddress(sell_token)
# Create token Instance for Token
sellTokenContract = web3.eth.contract(tokenToSell, abi=sellAbi)

# Get Token Balance
balance = sellTokenContract.functions.balanceOf(wallet_address).call()
symbol = sellTokenContract.functions.symbol().call()
readable = web3.fromWei(balance, 'ether')
print("Balance: " + str(readable) + " " + symbol)


random_amount = randint(100, 100)
# This is the Token(BNB) amount you want to Swap from
amount = random_amount/100
print(amount)


# # Approve Token before Selling
# start = time.time()
# approve = sellTokenContract.functions.approve(
#     panRouterContractAddress, balance
# ).buildTransaction({
#     'from': wallet_address,
#     'gasPrice': web3.toWei('5', 'gwei'),
#     'nonce': web3.eth.get_transaction_count(wallet_address),
# })

# signed_txn = web3.eth.account.sign_transaction(approve, private_key)
# tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
# print("Approved: " + web3.toHex(tx_token))
# # Wait after approve 10 seconds before sending transaction
# time.sleep(10)
# print(f"Swapping {amount} {symbol} for BNB")


pancakeswap2_txn = contract.functions.swapExactTokensForETH(
    web3.toWei(amount, 'ether'),
    0,
    [tokenToSell, spend],
    wallet_address,
    (int(time.time()) + 1000000)
).buildTransaction({
    'from': wallet_address,
    'gasPrice': web3.toWei('5', 'gwei'),
    'nonce': web3.eth.get_transaction_count(wallet_address),
})

signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Tx hash: " + web3.toHex(tx_token))

time.sleep(10)
balance = web3.eth.get_balance(wallet_address)
humanReadable = web3.fromWei(balance, 'ether')
print(f'Your ballance:  {humanReadable} BNB')
