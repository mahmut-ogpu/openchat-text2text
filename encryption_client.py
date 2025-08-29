import os
import time
import ogpu.client
from web3 import Web3
from typing import Optional


class OGPUEncryptionClient:
    """Client to call encryption service through OpenGPU task system"""
    
    def __init__(self, encryption_source_address: str):
        self.encryption_source_address = encryption_source_address
        self.timeout = 300  # 5 minutes timeout for encryption tasks
        
    def encrypt_text(self, text: str) -> str:
        """
        Encrypt text by creating an OpenGPU task for encryption service
        """
        try:
            # Create encryption task
            task_info = ogpu.client.TaskInfo(
                source=self.encryption_source_address,
                config=ogpu.client.TaskInput(
                    function_name="encrypt_text",
                    data={"text": text}
                ),
                expiryTime=int(time.time()) + self.timeout,
                payment=Web3.to_wei(0.001, "ether")  # Same as t2t service
            )
            
            # Publish task
            task_address = ogpu.client.publish_task(task_info)
            
            # Wait for response
            start_time = time.time()
            while time.time() - start_time < self.timeout:
                responses = ogpu.client.get_task_responses(task_address)
                
                # Check for completed response
                for response in responses:
                    if response.confirmed:
                        result_data = response.data
                        if result_data.get("success"):
                            return result_data.get("result", "")
                        else:
                            raise Exception(f"Encryption failed: {result_data.get('error_message')}")
                
                time.sleep(2)  # Poll every 2 seconds
            
            raise Exception("Encryption task timed out")
            
        except Exception as e:
            raise Exception(f"Failed to encrypt text: {e}")
    
    def decrypt_text(self, encrypted_text: str) -> str:
        """
        Decrypt text by creating an OpenGPU task for encryption service
        """
        try:
            # Create decryption task
            task_info = ogpu.client.TaskInfo(
                source=self.encryption_source_address,
                config=ogpu.client.TaskInput(
                    function_name="decrypt_text",
                    data={"encrypted_text": encrypted_text}
                ),
                expiryTime=int(time.time()) + self.timeout,
                payment=Web3.to_wei(0.001, "ether")  # Same as t2t service
            )
            
            # Publish task
            task_address = ogpu.client.publish_task(task_info)
            
            # Wait for response
            start_time = time.time()
            while time.time() - start_time < self.timeout:
                responses = ogpu.client.get_task_responses(task_address)
                
                # Check for completed response
                for response in responses:
                    if response.confirmed:
                        result_data = response.data
                        if result_data.get("success"):
                            return result_data.get("result", "")
                        else:
                            raise Exception(f"Decryption failed: {result_data.get('error_message')}")
                
                time.sleep(2)  # Poll every 2 seconds
            
            raise Exception("Decryption task timed out")
            
        except Exception as e:
            raise Exception(f"Failed to decrypt text: {e}")


# Environment variable approach for source address
def get_encryption_client() -> Optional[OGPUEncryptionClient]:
    """Get encryption client using environment variable for source address"""
    encryption_source = os.getenv('ENCRYPTION_SOURCE_ADDRESS')
    if encryption_source:
        return OGPUEncryptionClient(encryption_source)
    return None