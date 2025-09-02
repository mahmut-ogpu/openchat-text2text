# main.py
import ogpu.service
from models import EncryptRequest, DecryptRequest, CryptoResponse
from crypto_utils import AESCrypto

# Initialize crypto handler once at startup
crypto = None

@ogpu.service.init()
def setup():
    """Initialize the AES encryption system"""
    global crypto
    
    ogpu.service.logger.info("Initializing AES encryption service...")
    
    try:
        crypto = AESCrypto()
        ogpu.service.logger.info("AES encryption initialized successfully")
    except Exception as e:
        ogpu.service.logger.error(f"Failed to initialize encryption: {e}")
        raise e


@ogpu.service.expose()
def encrypt_text(request: EncryptRequest) -> CryptoResponse:
    """Encrypt plain text using AES-256-GCM"""
    
    ogpu.service.logger.info("Encrypting text...")
    
    try:
        if not crypto:
            raise Exception("Encryption not initialized")
        
        encrypted_result = crypto.encrypt(request.text)
        
        ogpu.service.logger.info("Text encrypted successfully")
        return CryptoResponse(
            result=encrypted_result,
            success=True
        )
        
    except Exception as e:
        error_msg = f"Encryption failed: {e}"
        ogpu.service.logger.error(error_msg)
        
        return CryptoResponse(
            result="",
            success=False,
            error_message=error_msg
        )


@ogpu.service.expose()
def decrypt_text(request: DecryptRequest) -> CryptoResponse:
    """Decrypt encrypted text using AES-256-GCM"""
    
    ogpu.service.logger.info("Decrypting text...")
    
    try:
        if not crypto:
            raise Exception("Encryption not initialized")
        
        decrypted_result = crypto.decrypt(request.encrypted_text)
        
        ogpu.service.logger.info("Text decrypted successfully")
        return CryptoResponse(
            result=decrypted_result,
            success=True
        )
        
    except Exception as e:
        error_msg = f"Decryption failed: {e}"
        ogpu.service.logger.error(error_msg)
        
        return CryptoResponse(
            result="",
            success=False,
            error_message=error_msg
        )


if __name__ == "__main__":
    ogpu.service.start()