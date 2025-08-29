# http_client.py
import requests
import json
from typing import Optional


class EncryptionClient:
    def __init__(self, encryption_service_url: str = "http://localhost:5556"):
        self.base_url = encryption_service_url.rstrip('/')
        self.timeout = 10  # seconds
    
    def encrypt_text(self, text: str) -> str:
        """
        Call encryption service to encrypt text
        Returns encrypted base64 string
        """
        try:
            url = f"{self.base_url}/encrypt"
            payload = {"text": text}
            
            response = requests.post(
                url, 
                json=payload, 
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result.get("result", "")
                else:
                    raise Exception(f"Encryption failed: {result.get('error_message')}")
            else:
                raise Exception(f"HTTP error {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error calling encryption service: {e}")
        except Exception as e:
            raise Exception(f"Encryption service error: {e}")
    
    def decrypt_text(self, encrypted_text: str) -> str:
        """
        Call encryption service to decrypt text
        Returns plain text string
        """
        try:
            url = f"{self.base_url}/decrypt"
            payload = {"encrypted_text": encrypted_text}
            
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result.get("result", "")
                else:
                    raise Exception(f"Decryption failed: {result.get('error_message')}")
            else:
                raise Exception(f"HTTP error {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error calling encryption service: {e}")
        except Exception as e:
            raise Exception(f"Decryption service error: {e}")


# Test function for local testing
def test_encryption_client():
    """Test the encryption client locally"""
    client = EncryptionClient("http://localhost:5555")  # Encryption service port
    
    test_message = "Hello, this is a test message!"
    print(f"Original: {test_message}")
    
    try:
        # Test encryption
        encrypted = client.encrypt_text(test_message)
        print(f"Encrypted: {encrypted[:50]}...")
        
        # Test decryption
        decrypted = client.decrypt_text(encrypted)
        print(f"Decrypted: {decrypted}")
        
        if test_message == decrypted:
            print("✅ Encryption client works correctly")
        else:
            print("❌ Mismatch in encryption/decryption")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_encryption_client()