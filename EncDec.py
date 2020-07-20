# inspired by
# https://nitratine.net/blog/post/encryption-and-decryption-in-python

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class EncDec:
    def __init__(self):
        self.salt = os.urandom(16)

    def _generate_key(self, _password: str):
        _password = _password.encode()  # convert to type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.b64encode(kdf.derive(_password))

    def _set_salt_from_crypttext(self, crypttext: str):
        self.salt = base64.b64decode((crypttext[0:22] + "==").encode())

    def _add_salt_to_crypttext(self, crypttext: str) -> str:
        return base64.b64encode(self.salt).decode("UTF-8")[0:22] + crypttext

    def encrypt(self, cleartext: str, _password: str) -> str:
        fernet = Fernet(self._generate_key(_password))
        return self._add_salt_to_crypttext(fernet.encrypt(cleartext.encode()).decode("UTF-8"))

    def decrypt(self, crypttext: str, _password: str) -> str:
        self._set_salt_from_crypttext(crypttext)
        fernet = Fernet(self._generate_key(_password))
        crypttext = crypttext[22:]  # remove salt
        return fernet.decrypt(crypttext.encode()).decode("UTF-8")
