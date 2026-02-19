from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('ENCRYPTION_KEY').encode()
cipher = Fernet(key)

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    return cipher.decrypt(encrypted_data.encode()).decode()