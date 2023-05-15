from web3 import Web3
import json
import requests

# Update the following variables with your own Etherscan and BscScan API keys and Telegram bot token
ETHERSCAN_API_KEY = 'IPMS9STM3WNJ4K55KR6FS1F1KB77VPI96K'
BSCSCAN_API_KEY = '97H84KY4GJ81VK591B3TKSFXG4ANTWYRV3'
FANTOM_API_KEY = 'XGH2V15G4WS9G6F13SN5R86UMA8FJURB92'
TELEGRAM_BOT_TOKEN = '5800403587:AAHHpzfKWVyheYYIWcMHpUJsMlqIhQ7xoTM'
TELEGRAM_CHAT_ID = '-984543212'


# Router address

ETH_ROUTER_ADDRESS = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
BSC_ROUTER_ADDRESS = '0x10ED43C718714eb63d5aA57B78B54704E256024E'


# Connect to the Ethereum network
eth_w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'))
eth_router = Web3.to_checksum_address('0x7a250d5630b4cf539739df2c5dacb4c659f2488d')
eth_usdt = Web3.to_checksum_address('0xdac17f958d2ee523a2206206994597c13d831ec7')
eth_weth = Web3.to_checksum_address('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')

bsc_w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
bsc_router = Web3.to_checksum_address('0x10ED43C718714eb63d5aA57B78B54704E256024E')
bsc_usdt = Web3.to_checksum_address('0x55d398326f99059ff775485246999027b3197955')
bsc_wbnb = Web3.to_checksum_address('0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c')

Round = lambda x, n: float(eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n))))

eth_abi = ''
with open('abi.json', 'r') as f:
    eth_abi = json.load(f)

router_abi = ''
with open('router.json', 'r') as f:
    router_abi = json.load(f)




def get_eth_tokensymbol(token_address):
    # Create a contract instance for the token
    token_address = Web3.to_checksum_address(token_address)
    token_contract = eth_w3.eth.contract(address=token_address, abi=eth_abi)
    # Call the name() function on the token contract
    token_name = token_contract.functions.symbol().call()
    return token_name

def get_bsc_tokensymbol(token_address):
    # Create a contract instance for the token
    token_address = Web3.to_checksum_address(token_address)
    token_contract = bsc_w3.eth.contract(address=token_address, abi=eth_abi)
    # Call the name() function on the token contract
    token_name = token_contract.functions.symbol().call()
    return token_name

def get_eth_tokendecimal(token_address):
    # Load the token contract ABI
    with open('abi.json', 'r') as f:
        token_abi = json.load(f)
    token_address = Web3.to_checksum_address(token_address)
    # Create a contract instance for the token
    token_contract = eth_w3.eth.contract(address=token_address, abi=token_abi)
    # Call the name() function on the token contract
    decimals = token_contract.functions.decimals().call()
    return int(decimals)


def get_bnb_price():
    router_contract = bsc_w3.eth.contract(address=bsc_router, abi=router_abi)
    oneToken = bsc_w3.to_wei(1, 'Ether')
    price = router_contract.functions.getAmountsOut(oneToken,
                                                   [bsc_wbnb,bsc_usdt]).call()
    normalizedPrice = bsc_w3.from_wei(price[1], 'Ether') / oneToken
    return Round((normalizedPrice) * 10 ** 18,2)

def get_eth_price():
    router_contract = eth_w3.eth.contract(address=eth_router, abi=router_abi)
    oneToken = eth_w3.to_wei(1, 'Ether')
    price = router_contract.functions.getAmountsOut(oneToken,
                                                    [eth_weth, eth_usdt]).call()
    return Round((price[1]) / 10 ** 6,2)

