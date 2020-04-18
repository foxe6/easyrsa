from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_512
from Crypto.Signature import PKCS1_v1_5
from omnitools import str_or_bytes, b64e, b64d, try_utf8d, try_utf8e, jl, jd_and_utf8e, utf8d, bytes_or_list


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
        except Exception as e:
            raise e
        finally:
            self.key = None

    def max_msg_size(self) -> int:
        try:
            if self.public_key:
                return RSA.import_key(self.public_key).n.bit_length()//8-42
            elif self.private_key:
                return RSA.import_key(self.private_key).n.bit_length()//8-42
        except Exception as e:
            raise e
        finally:
            self.private_key = None
            self.public_key = None

    def encrypt(self, v: str_or_bytes) -> bytes:
        if len(try_utf8e(v)) > EasyRSA(public_key=self.public_key).max_msg_size():
            return self.encryptlong(v)
        if isinstance(self.public_key, str):
            self.public_key = b64d(self.public_key)
        v = try_utf8e(v)
        return PKCS1_OAEP.new(RSA.import_key(self.public_key)).encrypt(v)

    def encryptlong(self, v: str_or_bytes) -> bytes:
        max_msg_size = EasyRSA(public_key=self.public_key).max_msg_size()
        parts = []
        while v:
            parts.append(b64e(self.encrypt(v[:max_msg_size])))
            v = v[max_msg_size:]
        return jd_and_utf8e(parts)

    def decrypt(self, v: bytes) -> str_or_bytes:
        try:
            return self.decryptlong(jl(utf8d(v)))
        except:
            pass
        if isinstance(self.private_key, str):
            self.private_key = b64d(self.private_key)
        v = PKCS1_OAEP.new(RSA.import_key(self.private_key)).decrypt(v)
        return try_utf8d(v)

    def decryptlong(self, parts: bytes_or_list) -> str_or_bytes:
        v = []
        for part in parts:
            v.append(self.decrypt(b64d(part)))
        if isinstance(v[0], str):
            return "".join(v)
        else:
            return b"".join(v)

    def sign(self, msg: str_or_bytes) -> bytes:
        return PKCS1_v1_5.new(RSA.import_key(self.private_key)).sign(SHA3_512.new(try_utf8e(msg)))

    def verify(self, msg: str_or_bytes, sig: bytes) -> bool:
        return PKCS1_v1_5.new(RSA.importKey(self.public_key).publickey()).verify(SHA3_512.new(try_utf8e(msg)), sig)


