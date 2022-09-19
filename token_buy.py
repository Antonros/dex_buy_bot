import os
import time
from random import randint

import telegram
from dotenv import load_dotenv
from schedule import every, repeat, run_pending
from web3 import Web3

from data import bnb_token_address, panabi, panRouterContractAddress


@repeat(every(20).to(80).seconds)
def job():

    buy_token = '0xe9e7cea3dedca5984780bafc599bd69add087d56'

    #  Случайным образом выбираем кошелек с которого покупаем
    random_wallet = randint(1, 2)
    print(random_wallet)

    bsc = 'https://bsc-dataseed.binance.org/'
    web3 = Web3(Web3.HTTPProvider(bsc))
    print(web3.isConnected())

    load_dotenv()

    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    WALLET = os.getenv('WALLET_' + str(random_wallet)).split('||')

    wallet_address = str(WALLET[0])
    private_key = str(WALLET[1])

    #  извлекаем и печатаем балланс кошелька
    balance = web3.eth.get_balance(wallet_address)
    humanReadable = web3.fromWei(balance, 'ether')
    print(f'Your ballance:  {humanReadable} BNB')

    random_amount = randint(10, 100)
    # This is the Token(BNB) amount you want to Swap from
    amount = random_amount/10000
    print(amount)

    tokenToBuy = web3.toChecksumAddress(buy_token)
    spend = web3.toChecksumAddress(bnb_token_address)

    # # Setup the PancakeSwap contract
    # contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)

    # pancakeswap2_txn = contract.functions.swapExactETHForTokens(
    #     0,
    #     [spend, tokenToBuy],
    #     wallet_address,
    #     (int(time.time()) + 10000)
    # ).buildTransaction({
    #     'from': wallet_address,
    #     'value': web3.toWei(amount, 'ether'),
    #     'gas': 250000,
    #     'gasPrice': web3.toWei('5', 'gwei'),
    #     'nonce': web3.eth.get_transaction_count(wallet_address),
    # })

    # signed_txn = web3.eth.account.sign_transaction(
    #     pancakeswap2_txn, private_key
    # )
    # tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # print("Tx hash: " + web3.toHex(tx_token))

    # time.sleep(10)
    # balance = web3.eth.get_balance(wallet_address)
    # humanReadable = web3.fromWei(balance, 'ether')
    # print(f'Your ballance:  {humanReadable} BNB')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text='message-test',
        )
    except telegram.TelegramError as error:
        raise Exception(f'Сообщение не отправлено, "{error}".')



while True:
    run_pending()
    time.sleep(1)
