from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_512
from Crypto.Signature import PKCS1_v1_5
from omnitools import *


__ALL__ = ["EasyRSA"]


class EasyRSA(object):
    def __init__(self, bits: int = None,
                 public_key: str_or_bytes = None,
                 private_key: str_or_bytes = None) -> None:
        if not ((public_key is None and private_key is None and bits is not None) or
                (bits is None and private_key is None and public_key is not None) or
                (public_key is None and bits is None and private_key is not None)):
            raise Exception("only one operation per init is allowed")
        self.key = bits
        self.public_key = public_key
        self.private_key = private_key

    def gen_key_pair(self):
        self.key = RSA.generate(bits=self.key)
        try:
            return dict(
                private_key=self.key.export_key(),
                public_key=self.key.publickey().export_key()
            )
        finally:
            self.key = None

    def encrypt(self, v: str_or_bytes) -> bytes:
        if isinstance(self.public_key, str):
            self.public_key = b64d(self.public_key)
        v = try_utf8e(v)
        return PKCS1_OAEP.new(RSA.import_key(self.public_key)).encrypt(v)

    def decrypt(self, v: str_or_bytes) -> str_or_bytes:
        if isinstance(self.private_key, str):
            self.private_key = b64d(self.private_key)
        if isinstance(v, str):
            v = b64d(v)
        v = PKCS1_OAEP.new(RSA.import_key(self.private_key)).decrypt(v)
        return try_utf8d(v)

    def sign(self, msg: str_or_bytes) -> bytes:
        return PKCS1_v1_5.new(RSA.import_key(self.private_key)).sign(SHA3_512.new(try_utf8e(msg)))

    def verify(self, msg: str_or_bytes, sig: bytes) -> bool:
        return PKCS1_v1_5.new(RSA.importKey(self.public_key).publickey()).verify(SHA3_512.new(try_utf8e(msg)), sig)


