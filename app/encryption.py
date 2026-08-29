import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv


load_dotenv()

key = os.getenv("ENCRYPTION_KEY")

cipher = Fernet(key)


def encrypt_data(data: str) -> str:
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data.decode()


def decrypt_data(encrypted_data: str) -> str:
    decrypted_data = cipher.decrypt(encrypted_data.encode())
    return decrypted_data.decode()