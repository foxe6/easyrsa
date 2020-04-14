# Easy RSA

<badges>[![version](https://img.shields.io/pypi/v/easyrsa.svg)](https://pypi.org/project/easyrsa/)
[![license](https://img.shields.io/pypi/l/easyrsa.svg)](https://pypi.org/project/easyrsa/)
[![pyversions](https://img.shields.io/pypi/pyversions/easyrsa.svg)](https://pypi.org/project/easyrsa/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Encrypt symmetric keys with RSA.</i>

# Hierarchy

```
easyrsa
'---- EasyRSA()
    |---- gen_private_key()
    |---- gen_public_key()
    |---- encrypt()
    |---- decrypt()
    |---- sign()
    '---- verify()
```

# Example

## python
```python
from easyrsa import *

# generate a key pair
kp = EasyRSA(bits=512*2).gen_key_pair()
print(kp)
# {"public_key": b"...", "private_key": b"..."}

# encryption and decryption
# note that each EasyRSA object must bind only one operation
# EasyRSA fails to operate if more than one argument are passed in
from base64 import b64encode
symmetric_key = "abc" or b"abc" or b64encode(b"abc")
encrypted_key = EasyRSA(public_key=kp["public_key"]).encrypt(symmetric_key)
key_in_b64 = b64encode(encrypted_key).decode("utf-8")
print(encrypted_key)
# ...
print(key_in_b64)
# ...
print(symmetric_key == EasyRSA(private_key=kp["private_key"]).decrypt(encrypted_key))
# True
print(symmetric_key == EasyRSA(private_key=kp["private_key"]).decrypt(key_in_b64))
# True

# sign and verify
msg = randb(1024)
s = EasyRSA(private_key=kp["private_key"]).sign(msg)
# and then somehow you receive the msg
print(EasyRSA(public_key=kp["public_key"]).verify(msg, s))
# True
```

## shell
```shell script
rem easyrsa.exe {private key in base64|public key in base64} {base64 string to decrypt|symmetric key to encrypt}
easyrsa.exe <private key in base64> <base64 string to decrypt>
rem decryption returns string
easyrsa.exe <public key in base64> <symmetric key to encrypt>
rem encryption returns string in b64
```