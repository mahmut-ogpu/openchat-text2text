# generate_wallet.py
from web3 import Web3
import secrets

def generate_new_wallet():
    """Generate a new Ethereum wallet"""
    
    # Generate random private key (32 bytes = 64 hex characters)
    private_key_bytes = secrets.token_bytes(32)
    private_key = "0x" + private_key_bytes.hex()
    
    # Create account from private key
    account = Web3().eth.account.from_key(private_key)
    
    print("New wallet generated:")
    print(f"Private Key: {private_key}")
    print(f"Address: {account.address}")
    print()
    print("IMPORTANT:")
    print("1. Save your private key securely")
    print("2. Never share your private key")
    print("3. You'll need testnet OGPU tokens at this address")
    print("4. Use this private key as CLIENT_PRIVATE_KEY")
    
    return private_key, account.address

if __name__ == "__main__":
    generate_new_wallet()