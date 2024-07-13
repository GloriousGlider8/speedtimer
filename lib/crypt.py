from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def aes256(data, passphrase, encrypt=True):
    # Derive key from passphrase using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=passphrase.encode(),  # Encode passphrase as bytes
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode())

    # Initialize AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\x00'*16), backend=default_backend())

    if encrypt:
        # Apply padding to data
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        # Encrypt data
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return ct
    else:
        # Decrypt data
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(data) + decryptor.finalize()

        # Unpad decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data