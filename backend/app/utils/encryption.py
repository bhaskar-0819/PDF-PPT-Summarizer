from cryptography.fernet import Fernet
import os

KEY_PATH = "secret.key"

def load_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as f:
            f.write(key)
    else:
        with open(KEY_PATH, "rb") as f:
            key = f.read()
    return key

key = load_key()
cipher = Fernet(key)

def encrypt_data(data: bytes) -> bytes:
    return cipher.encrypt(data)

def decrypt_data(data: bytes) -> bytes:
    return cipher.decrypt(data)