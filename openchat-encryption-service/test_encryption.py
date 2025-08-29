# test_encryption.py
import os
from crypto_utils import AESCrypto, generate_aes_key
from models import EncryptRequest, DecryptRequest

def test_encryption():
    """Test the encryption and decryption functionality"""
    
    # Generate a test key for demonstration
    test_key = generate_aes_key()
    print(f"Test key: {test_key}")
    
    # Set environment variable
    os.environ['AES_ENCRYPTION_KEY'] = test_key
    
    # Initialize crypto
    crypto = AESCrypto()
    
    # Test data
    test_messages = [
        "Hello, this is a secret message!",
        "What is the capital of France?",
        "This is a test of AES-256-GCM encryption",
        "Special characters: !@#$%^&*()"
    ]
    
    print("\n--- Testing Encryption/Decryption ---")
    
    for i, message in enumerate(test_messages):
        print(f"\nTest {i+1}:")
        print(f"Original: {message}")
        
        try:
            # Encrypt
            encrypted = crypto.encrypt(message)
            print(f"Encrypted: {encrypted[:50]}...")
            
            # Decrypt
            decrypted = crypto.decrypt(encrypted)
            print(f"Decrypted: {decrypted}")
            
            # Verify
            if message == decrypted:
                print("✅ Success: Original matches decrypted")
            else:
                print("❌ Failed: Mismatch!")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_encryption()