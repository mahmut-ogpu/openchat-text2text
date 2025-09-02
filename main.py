# main.py (modified text2text service for Docker integration)
import ollama
from ollama import chat
from ollama import ChatResponse
import os

import ogpu.service
from models import InputData, Message
from http_encryption_client import HTTPEncryptionClient

MODEL_NAME = "qwen2.5:3b"

# Global encryption client
encryption_client = None

@ogpu.service.init()
def setup():
    """Initialize Ollama, pull the model, and setup HTTP encryption client"""
    global encryption_client
    
    ogpu.service.logger.info(f"Pulling {MODEL_NAME} model...")
    ollama.pull(MODEL_NAME)
    ogpu.service.logger.info(f"{MODEL_NAME} pulled.")
    
    # Initialize HTTP encryption client for Docker integration
    ogpu.service.logger.info("Setting up HTTP encryption client...")
    try:
        # Use Docker service name for container-to-container communication
        encryption_url = os.getenv('ENCRYPTION_SERVICE_URL', 'http://openchat-encryption-service:5555')
        encryption_client = HTTPEncryptionClient(encryption_url)
        ogpu.service.logger.info(f"HTTP encryption client initialized with URL: {encryption_url}")
    except Exception as e:
        ogpu.service.logger.error(f"Failed to initialize HTTP encryption client: {e}")
        ogpu.service.logger.warning("Continuing without encryption")


def decrypt_messages(messages):
    """Decrypt all messages before sending to Ollama"""
    if not encryption_client:
        # No encryption - return messages as-is
        ogpu.service.logger.info("No encryption client - passing messages through unchanged")
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    
    decrypted_messages = []
    
    for message in messages:
        try:
            ogpu.service.logger.info(f"Decrypting message from role: {message.role}")
            # Decrypt the message content
            decrypted_content = encryption_client.decrypt_text(message.content)
            decrypted_message = {
                "role": message.role,
                "content": decrypted_content
            }
            decrypted_messages.append(decrypted_message)
            ogpu.service.logger.info(f"Successfully decrypted message from role: {message.role}")
            
        except Exception as e:
            ogpu.service.logger.error(f"Failed to decrypt message from {message.role}: {e}")
            # For testing, let's be more flexible - try to use message as-is if decryption fails
            ogpu.service.logger.warning("Using original message content as fallback")
            decrypted_message = {
                "role": message.role,
                "content": message.content  # Use original content as fallback
            }
            decrypted_messages.append(decrypted_message)
    
    return decrypted_messages


def encrypt_response(response_content):
    """Encrypt response before returning to client"""
    if not encryption_client:
        # No encryption - return content as-is
        ogpu.service.logger.info("No encryption client - returning response unchanged")
        return response_content
    
    try:
        ogpu.service.logger.info("Encrypting response...")
        encrypted_content = encryption_client.encrypt_text(response_content)
        ogpu.service.logger.info("Response encrypted successfully")
        return encrypted_content
        
    except Exception as e:
        ogpu.service.logger.error(f"Failed to encrypt response: {e}")
        ogpu.service.logger.warning("Returning unencrypted response as fallback")
        return response_content


@ogpu.service.expose()
def text2text(input_data: InputData) -> Message:
    """Generate text response using Ollama chat interface with HTTP encryption integration"""
    
    if encryption_client:
        ogpu.service.logger.info("Generating Text2Text response with HTTP encryption...")
    else:
        ogpu.service.logger.info("Generating Text2Text response without encryption...")

    try:
        # STEP 1: Decrypt incoming messages (if encryption is enabled)
        ogpu.service.logger.info("Processing incoming messages...")
        processed_messages = decrypt_messages(input_data.messages)
        
        # STEP 2: Send processed messages to Ollama (original logic unchanged)
        ogpu.service.logger.info("Sending messages to Ollama...")
        response: ChatResponse = chat(model=MODEL_NAME, messages=processed_messages)
        
        # STEP 3: Encrypt the response (if encryption is enabled)
        original_content = response['message']['content']
        ogpu.service.logger.info("Processing response...")
        
        final_content = encrypt_response(original_content)
        
        # STEP 4: Return response
        output = Message(
            role=response['message']['role'],
            content=final_content
        )

        ogpu.service.logger.info("Task completed successfully.")
        return output

    except Exception as e:
        ogpu.service.logger.error(f"An error occurred in text2text: {e}")
        raise e


if __name__ == "__main__":
    ogpu.service.start()