# test_published_encryption.py
import ogpu.client
import time
from web3 import Web3
import os

# Configure testnet
ogpu.client.ChainConfig.set_chain(ogpu.client.ChainId.OGPU_TESTNET)

def test_encryption_service():
    """Test the published encryption service on OpenGPU testnet"""
    
    # Your published source address
    source_address = "0xcfCF47eD54D1Ec3679a60Cd7E99F3B22f53774Da"
    
    print("Testing published encryption service...")
    print(f"Source address: {source_address}")
    
    try:
        # Test 1: Encrypt a message
        test_message = "Hello, this is a test message for the published encryption service!"
        print(f"\nTest 1 - Encrypting: '{test_message}'")
        
        encrypt_task = ogpu.client.TaskInfo(
            source=source_address,
            config=ogpu.client.TaskInput(
                function_name="encrypt_text",
                data={"text": test_message}
            ),
            expiryTime=int(time.time()) + 120,  # 2 minutes
            payment=Web3.to_wei(0.001, "ether")
        )
        
        # Publish encryption task
        encrypt_task_address = ogpu.client.publish_task(encrypt_task)
        print(f"Encryption task published: {encrypt_task_address}")
        print("Waiting for encryption result...")
        
        # Poll for encryption result
        encrypted_result = None
        for i in range(30):  # Wait up to 60 seconds
            time.sleep(2)
            responses = ogpu.client.get_task_responses(encrypt_task_address)
            
            for response in responses:
                if response.confirmed:
                    result_data = response.data
                    if result_data.get("success"):
                        encrypted_result = result_data.get("result")
                        print(f"✅ Encryption successful!")
                        print(f"Encrypted: {encrypted_result[:50]}...")
                        break
                    else:
                        print(f"❌ Encryption failed: {result_data.get('error_message')}")
                        return False
            
            if encrypted_result:
                break
            
            if i % 5 == 0:  # Print status every 10 seconds
                print(f"Still waiting... ({i*2}s)")
        
        if not encrypted_result:
            print("❌ Encryption task timed out")
            return False
        
        # Test 2: Decrypt the message
        print(f"\nTest 2 - Decrypting the encrypted result...")
        
        decrypt_task = ogpu.client.TaskInfo(
            source=source_address,
            config=ogpu.client.TaskInput(
                function_name="decrypt_text",
                data={"encrypted_text": encrypted_result}
            ),
            expiryTime=int(time.time()) + 120,  # 2 minutes
            payment=Web3.to_wei(0.001, "ether")
        )
        
        # Publish decryption task
        decrypt_task_address = ogpu.client.publish_task(decrypt_task)
        print(f"Decryption task published: {decrypt_task_address}")
        print("Waiting for decryption result...")
        
        # Poll for decryption result
        decrypted_result = None
        for i in range(30):  # Wait up to 60 seconds
            time.sleep(2)
            responses = ogpu.client.get_task_responses(decrypt_task_address)
            
            for response in responses:
                if response.confirmed:
                    result_data = response.data
                    if result_data.get("success"):
                        decrypted_result = result_data.get("result")
                        print(f"✅ Decryption successful!")
                        print(f"Decrypted: '{decrypted_result}'")
                        break
                    else:
                        print(f"❌ Decryption failed: {result_data.get('error_message')}")
                        return False
            
            if decrypted_result:
                break
            
            if i % 5 == 0:  # Print status every 10 seconds
                print(f"Still waiting... ({i*2}s)")
        
        if not decrypted_result:
            print("❌ Decryption task timed out")
            return False
        
        # Verify round-trip success
        if test_message == decrypted_result:
            print(f"\n🎉 SUCCESS! Round-trip encryption/decryption works perfectly!")
            print(f"Original:  '{test_message}'")
            print(f"Decrypted: '{decrypted_result}'")
            return True
        else:
            print(f"\n❌ FAILED! Messages don't match:")
            print(f"Original:  '{test_message}'")
            print(f"Decrypted: '{decrypted_result}'")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def check_balance():
    """Check if we have enough tokens for testing"""
    try:
        # This is a simple check - you might need to implement balance checking
        print("Checking wallet balance for testing...")
        print("Note: Make sure you have enough testnet OGPU for gas fees")
        return True
    except Exception as e:
        print(f"Could not check balance: {e}")
        return False

if __name__ == "__main__":
    # Make sure CLIENT_PRIVATE_KEY is set
    if not os.getenv('CLIENT_PRIVATE_KEY'):
        print("❌ Please set CLIENT_PRIVATE_KEY environment variable")
        print("Example: $env:CLIENT_PRIVATE_KEY='your_private_key_here'")
        exit(1)
    
    print("🧪 Testing Published Encryption Service on OpenGPU Testnet")
    print("=" * 60)
    
    if check_balance():
        success = test_encryption_service()
        
        if success:
            print("\n✅ All tests passed! Your encryption service is working correctly.")
            print("\nNext steps:")
            print("1. Save the source address: 0x07F3C688B07f19989284792Cf65aEe7d1a975aA7")
            print("2. Update your text2text service to use this encryption service")
            print("3. Test the integrated system")
        else:
            print("\n❌ Tests failed. Check the errors above.")
            print("The service might need time to start or there could be configuration issues.")