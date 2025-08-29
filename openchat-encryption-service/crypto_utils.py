import os
import base64
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AESCrypto:
    def __init__(self):
        # Load AES key from environment variable
        key_string = os.getenv('AES_ENCRYPTION_KEY')
        if not key_string:
            raise ValueError("AES_ENCRYPTION_KEY environment variable is required")
        
        # Convert hex string to bytes (expecting 64 hex chars for 32 bytes)
        try:
            self.key = bytes.fromhex(key_string)
            if len(self.key) != 32:
                raise ValueError("AES key must be 32 bytes (64 hex characters)")
        except ValueError as e:
            raise ValueError(f"Invalid AES key format: {e}")
        
        self.aesgcm = AESGCM(self.key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using AES-256-GCM
        Returns base64 encoded: nonce + encrypted_data + auth_tag
        """
        try:
            # Generate random 12-byte nonce
            nonce = secrets.token_bytes(12)
            
            # Convert string to bytes
            plaintext_bytes = plaintext.encode('utf-8')
            
            # Encrypt with AES-GCM (includes authentication)
            ciphertext = self.aesgcm.encrypt(nonce, plaintext_bytes, None)
            
            # Combine nonce + ciphertext (ciphertext already includes auth tag)
            combined = nonce + ciphertext
            
            # Return as base64 string
            return base64.b64encode(combined).decode('ascii')
            
        except Exception as e:
            raise Exception(f"Encryption failed: {e}")
    
    def decrypt(self, encrypted_base64: str) -> str:
        """
        Decrypt base64 encoded encrypted data
        Expects format: nonce + encrypted_data + auth_tag
        """
        try:
            # Decode from base64
            combined = base64.b64decode(encrypted_base64.encode('ascii'))
            
            # Extract nonce (first 12 bytes)
            nonce = combined[:12]
            
            # Extract ciphertext (remaining bytes, includes auth tag)
            ciphertext = combined[12:]
            
            # Decrypt with AES-GCM (automatically verifies authentication)
            plaintext_bytes = self.aesgcm.decrypt(nonce, ciphertext, None)
            
            # Convert bytes back to string
            return plaintext_bytes.decode('utf-8')
            
        except Exception as e:
            raise Exception(f"Decryption failed: {e}")


def generate_aes_key() -> str:
    """
    Generate a new 256-bit AES key and return as hex string
    Use this once to generate your encryption key
    """
    key_bytes = secrets.token_bytes(32)  # 256 bits
    return key_bytes.hex()


# Example usage for key generation (run this once)
if __name__ == "__main__":
    new_key = generate_aes_key()
    print(f"Generated AES key: {new_key}")
    print("Set this as your AES_ENCRYPTION_KEY environment variable")