import os

import telegram
from dotenv import load_dotenv
from web3 import Web3

from data import sellAbi

bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def get_bnb_balance(wallet_address):
    balance = web3.eth.get_balance(wallet_address)
    return round(web3.fromWei(balance, 'ether'), 3)


def get_token_balance(token, wallet_address):
    # Create token Instance for Token
    TokenContract = web3.eth.contract(token, abi=sellAbi)
    # Get Token Balance
    balance = TokenContract.functions.balanceOf(wallet_address).call()
    # symbol = TokenContract.functions.symbol().call()
    return round(web3.fromWei(balance, 'ether'), 3)


def telegram_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
    except telegram.TelegramError as error:
        raise Exception(f'Сообщение не отправлено, "{error}".')
