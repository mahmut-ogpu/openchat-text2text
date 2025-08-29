import ogpu.client
from web3 import Web3

def publish_encryption_service():
    """Publish encryption service to OpenGPU testnet"""
    
    # Configure for testnet
    ogpu.client.ChainConfig.set_chain(ogpu.client.ChainId.OGPU_TESTNET)
    
    print("Publishing encryption service to OpenGPU testnet...")
    
    # Create source info
    source_info = ogpu.client.SourceInfo(
        name="openchat-encryption",
        description="AES-256-GCM encryption/decryption service for secure message processing",
        logoUrl="https://raw.githubusercontent.com/OpenGPU-Network/assets/main/ogpu-logo.png",
        imageEnvs=ogpu.client.ImageEnvironments(
            # You need to upload your docker-compose file to a public URL
            # For now using a placeholder - you'll need to replace this
            cpu="https://raw.githubusercontent.com/mahmut-ogpu/openchat-text2text/main/docker-compose/encryption-cpu.yml"
        ),
        minPayment=Web3.to_wei(0.001, "ether"),  # Same as text2text service
        minAvailableLockup=Web3.to_wei(0, "ether"),
        maxExpiryDuration=300,  # 5 minutes (encryption should be fast)
        deliveryMethod=ogpu.client.DeliveryMethod.FIRST_RESPONSE,  # Automatic for deterministic operations
    )
    
    try:
        # Publish the source
        source_address = ogpu.client.publish_source(source_info)
        
        print(f"✅ Encryption service published successfully!")
        print(f"📍 Source address: {source_address}")
        print(f"🔗 Explorer: https://ogpuscan.io/source/{source_address}")
        print(f"💰 Payment: 0.001 OGPU per task")
        print(f"⏱️  Timeout: 5 minutes")
        
        return source_address
        
    except Exception as e:
        print(f"❌ Failed to publish source: {e}")
        return None

if __name__ == "__main__":
    # Make sure your CLIENT_PRIVATE_KEY is set in environment
    import os
    if not os.getenv('CLIENT_PRIVATE_KEY'):
        print("❌ Please set CLIENT_PRIVATE_KEY environment variable")
        print("Example: $env:CLIENT_PRIVATE_KEY='your_private_key_here'")
        exit(1)
    
    source_address = publish_encryption_service()
    
    if source_address:
        print("\n📝 Next steps:")
        print("1. Save this source address for your text2text service")
        print("2. Test the encryption service with a simple task")
        print("3. Update your text2text service configuration")