import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from secretsharing import SecretSharer

import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from secretsharing import SecretSharer

# 🧱 Padding and Unpadding (PKCS7)
def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Invalid padding.")
    return data[:-pad_len]

# 🔑 Generate a secure AES key and IV
def generate_aes_key_and_iv():
    key = get_random_bytes(32)  # 256-bit AES key
    iv = get_random_bytes(16)   # 128-bit IV (AES block size)
    return key, iv

# 🔐 Encrypt vote text using AES-256-CBC
def encrypt_vote(plaintext_vote):
    key, iv = generate_aes_key_and_iv()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext_vote.encode('utf-8'))
    ciphertext = cipher.encrypt(padded)
    return {
        "ciphertext_b64": base64.b64encode(ciphertext).decode('utf-8'),
        "iv_b64": base64.b64encode(iv).decode('utf-8'),
        "key_hex": key.hex()  # This key should be split into shares
    }


# 🔓 Decrypt the ciphertext using the reconstructed AES key and IV
def decrypt_vote(ciphertext_b64, key_hex, iv_b64):
    key = bytes.fromhex(key_hex)
    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return unpad(plaintext).decode('utf-8')

# 🧩 Split the AES key into Shamir shares
def split_key_into_shares(key_hex, threshold=3, total=5):
    return SecretSharer.split_secret(key_hex, threshold, total)

# 🔁 Reconstruct the AES key from Shamir shares
def reconstruct_aes_key(shares):
    return SecretSharer.recover_secret(shares)




