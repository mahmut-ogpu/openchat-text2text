# http_encryption_client.py
import requests
import json
import time
from typing import Optional


class HTTPEncryptionClient:
    """HTTP client to call encryption service directly for local Docker testing"""
    
    def __init__(self, encryption_service_url: str = "http://openchat-encryption-service:5555"):
        self.base_url = encryption_service_url.rstrip('/')
        self.timeout = 30  # seconds
    
    def encrypt_text(self, text: str) -> str:
        """
        Call encryption service via HTTP to encrypt text
        Returns encrypted base64 string
        """
        try:
            # For local testing, we'll call the service's task endpoint directly
            url = f"{self.base_url}/run/encrypt_text/test_task"
            
            # Create the request payload matching OpenGPU format
            payload = {
                "text": text
            }
            
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
        Call encryption service via HTTP to decrypt text  
        Returns plain text string
        """
        try:
            url = f"{self.base_url}/run/decrypt_text/test_task"
            
            payload = {
                "encrypted_text": encrypted_text
            }
            
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


# Test function for local Docker testing
def test_http_encryption_client():
    """Test the HTTP encryption client locally"""
    client = HTTPEncryptionClient("http://localhost:5556")  # For local testing
    
    test_message = "Hello, this is a Docker integration test!"
    print(f"Testing HTTP encryption client...")
    print(f"Original: {test_message}")
    
    try:
        # Test encryption
        encrypted = client.encrypt_text(test_message)
        print(f"Encrypted: {encrypted[:50]}...")
        
        # Test decryption
        decrypted = client.decrypt_text(encrypted)
        print(f"Decrypted: {decrypted}")
        
        if test_message == decrypted:
            print("✅ HTTP encryption client works correctly")
        else:
            print("❌ Mismatch in encryption/decryption")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_http_encryption_client()