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
    |---- gen_key_pair()
    |---- encrypt()
    |---- decrypt()
    |---- sign()
    |---- verify()
    '---- max_msg_size()
```

# Example

## python
```python
from easyrsa import *

# generate a key pair
kp = EasyRSA(bits=1024).gen_key_pair()
print(kp)
# {"public_key": b"...", "private_key": b"..."}

# maximum message size in bytes encrypted with a n bits RSA key
print(EasyRSA(public_key=kp["public_key"]).max_msg_size())
# 86
print(EasyRSA(private_key=kp["private_key"]).max_msg_size())
# 86

# encryption and decryption
# note that each EasyRSA object must bind only one operation
from base64 import b64encode
symmetric_key = "abc" or b"abc"*100 or b64encode(b"abc")
encrypted_key = EasyRSA(public_key=kp["public_key"]).encrypt(symmetric_key)
print(encrypted_key)
# ...
print(symmetric_key == EasyRSA(private_key=kp["private_key"]).decrypt(encrypted_key))
# True

# sign and verify
msg = "encrypted"
s = EasyRSA(private_key=kp["private_key"]).sign(msg)
# and then somehow you receive the msg
print(EasyRSA(public_key=kp["public_key"]).verify(msg, s))
# True
```
