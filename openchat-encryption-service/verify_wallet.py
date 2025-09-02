# verify_wallet.py
from web3 import Web3
import os

private_key = os.getenv('CLIENT_PRIVATE_KEY')
account = Web3().eth.account.from_key(private_key)
print(f"Publishing with address: {account.address}")