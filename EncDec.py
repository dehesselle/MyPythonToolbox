# inspired by
# https://nitratine.net/blog/post/encryption-and-decryption-in-python

from base64 import b64decode, b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from os import urandom


def generate_key(password: str, salt: bytes):
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return b64encode(kdf.derive(password))


def encrypt(cleartext: str, password: str) -> str:
    salt = urandom(16)
    fernet = Fernet(generate_key(password, salt))
    return (b64encode(salt)[0:22] + b64encode(fernet.encrypt(cleartext.encode()))).decode("UTF-8")


def decrypt(crypttext: str, password: str) -> str:
    salt = b64decode((crypttext[0:22] + "==").encode())
    crypttext = crypttext[22:]  # remove salt
    fernet = Fernet(generate_key(password, salt))
    return fernet.decrypt(b64decode(crypttext.encode())).decode("UTF-8")
