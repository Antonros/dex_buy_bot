import os
import time
from random import randint

from dotenv import load_dotenv
from schedule import every, repeat, run_pending
from web3 import Web3

from data import bnb_token_address, panabi, panRouterContractAddress
from functions import get_bnb_balance, get_token_balance, telegram_message

bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

load_dotenv()
TOKEN = os.getenv('TOKEN')


@repeat(every(2).to(3).seconds)
def job():

    #  Случайным образом выбираем кошелек с которого производим действие
    random_wallet = randint(3, 32)
    WALLET = os.getenv('WALLET_' + str(random_wallet)).split('||')

    wallet_address = str(WALLET[0])
    private_key = str(WALLET[1])

    sell(random_wallet, wallet_address, private_key)


def sell(random_wallet, wallet_address, private_key):

    message = 'SELL wallet ' + str(random_wallet) + '\n'
    #  извлекаем и печатаем балланс кошелька
    message += ('BNB balance: ' + str(get_bnb_balance(wallet_address)) + '\n')

    tokenToSell = web3.toChecksumAddress(TOKEN)

    # Get Token Balance
    message += (
        'Token balance: ' +
        str(get_token_balance(tokenToSell, wallet_address)) +
        '\n'
    )

    balance_amount = get_token_balance(tokenToSell, wallet_address)

    if balance_amount < 2:
        message += 'Балланса токена недостаточно для продажи'
        print(message)
        return

    balance_amount = balance_amount - 1

    # This is the Token amount you want to Swap from
    amount = int(balance_amount*1000000000000000000)  # 18 нулей

    message += 'Token spend: ' + str(balance_amount) + '\n'
    telegram_message(message)
    spend = web3.toChecksumAddress(bnb_token_address)

    # Setup the PancakeSwap contract
    contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)

    pancakeswap2_txn = contract.functions.swapExactTokensForETH(
        amount,
        0,
        [tokenToSell, spend],
        wallet_address,
        (int(time.time()) + 1000000)
    ).buildTransaction({
        'from': wallet_address,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(
        pancakeswap2_txn, private_key
    )
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    message += 'Tx hash: ' + web3.toHex(tx_token) + '\n'

    time.sleep(10)

    message += (
        'BNB balance: ' +
        str(get_bnb_balance(wallet_address)) + ' BNB' +
        '\n'
    )
    # Get Token Balance
    message += (
        'Token balance: ' +
        str(get_token_balance(tokenToSell, wallet_address)) +
        '\n'
    )

    print(message)
    telegram_message(message)


while True:
    run_pending()
    time.sleep(1)
