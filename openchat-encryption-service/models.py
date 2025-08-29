from pydantic import BaseModel
from typing import Optional


class EncryptRequest(BaseModel):
    text: str


class DecryptRequest(BaseModel):
    encrypted_text: str


class CryptoResponse(BaseModel):
    result: str
    success: bool
    error_message: Optional[str] = None