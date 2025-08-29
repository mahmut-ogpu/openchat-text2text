import ollama
from ollama import chat
from ollama import ChatResponse
import os

import ogpu.service
from .models import InputData, Message
from .encryption_client import get_encryption_client

MODEL_NAME = "qwen2.5:3b"

# Global encryption client
encryption_client = None

@ogpu.service.init()
def setup():
    """Initialize Ollama, pull the model, and setup encryption client"""
    global encryption_client
    
    ogpu.service.logger.info(f"Pulling {MODEL_NAME} model...")
    ollama.pull(MODEL_NAME)
    ogpu.service.logger.info(f"{MODEL_NAME} pulled.")
    
    # Initialize encryption client if source address is provided
    ogpu.service.logger.info("Setting up encryption client...")
    try:
        encryption_client = get_encryption_client()
        if encryption_client:
            ogpu.service.logger.info("Encryption client initialized successfully")
        else:
            ogpu.service.logger.warning("ENCRYPTION_SOURCE_ADDRESS not set - encryption disabled")
    except Exception as e:
        ogpu.service.logger.error(f"Failed to initialize encryption client: {e}")
        # Don't fail startup if encryption setup fails
        ogpu.service.logger.warning("Continuing without encryption")


def decrypt_messages(messages):
    """Decrypt all messages before sending to Ollama"""
    if not encryption_client:
        # No encryption - return messages as-is
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    
    decrypted_messages = []
    
    for message in messages:
        try:
            # Decrypt the message content
            decrypted_content = encryption_client.decrypt_text(message.content)
            decrypted_message = {
                "role": message.role,
                "content": decrypted_content
            }
            decrypted_messages.append(decrypted_message)
            ogpu.service.logger.info(f"Decrypted message from role: {message.role}")
            
        except Exception as e:
            ogpu.service.logger.error(f"Failed to decrypt message: {e}")
            # For robustness, you could try to use the message as-is if decryption fails
            # For security, we'll fail the entire request
            raise Exception(f"Message decryption failed: {e}")
    
    return decrypted_messages


def encrypt_response(response_content):
    """Encrypt response before returning to client"""
    if not encryption_client:
        # No encryption - return content as-is
        return response_content
    
    try:
        encrypted_content = encryption_client.encrypt_text(response_content)
        ogpu.service.logger.info("Response encrypted successfully")
        return encrypted_content
        
    except Exception as e:
        ogpu.service.logger.error(f"Failed to encrypt response: {e}")
        raise Exception(f"Response encryption failed: {e}")


@ogpu.service.expose()
def text2text(input_data: InputData) -> Message:
    """Generate text response using Ollama chat interface with optional encryption"""
    
    if encryption_client:
        ogpu.service.logger.info("Generating Text2Text response with encryption...")
    else:
        ogpu.service.logger.info("Generating Text2Text response without encryption...")

    try:
        # STEP 1: Decrypt incoming messages (if encryption is enabled)
        if encryption_client:
            ogpu.service.logger.info("Decrypting incoming messages...")
        
        processed_messages = decrypt_messages(input_data.messages)
        
        # STEP 2: Send processed messages to Ollama (original logic unchanged)
        ogpu.service.logger.info("Sending messages to Ollama...")
        response: ChatResponse = chat(model=MODEL_NAME, messages=processed_messages)
        
        # STEP 3: Encrypt the response (if encryption is enabled)
        original_content = response['message']['content']
        
        if encryption_client:
            ogpu.service.logger.info("Encrypting response...")
            final_content = encrypt_response(original_content)
        else:
            final_content = original_content
        
        # STEP 4: Return response
        output = Message(
            role=response['message']['role'],
            content=final_content
        )

        ogpu.service.logger.info("Task completed.")
        return output

    except Exception as e:
        ogpu.service.logger.error(f"An error occurred: {e}")
        raise e


if __name__ == "__main__":
    ogpu.service.start()