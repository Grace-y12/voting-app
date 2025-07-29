# vote/utils/keys.py

import hashlib
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

# Deterministic random generator using SHA256
def deterministic_rng(seed: bytes):
    h = SHA256.new(seed)
    while True:
        h = SHA256.new(h.digest())
        yield h.digest()

class DeterministicRandom:
    def __init__(self, seed):
        self.generator = deterministic_rng(seed)
        self.buffer = b""

    def read(self, n):
        while len(self.buffer) < n:
            self.buffer += next(self.generator)
        result = self.buffer[:n]
        self.buffer = self.buffer[n:]
        return result

# Main keypair generator
def generate_deterministic_key_pair(username, password):
    seed = hashlib.sha256((username + password).encode()).digest()
    randfunc = DeterministicRandom(seed).read
    key = RSA.generate(2048, randfunc=randfunc)
    private_pem = key.export_key().decode()
    public_pem = key.publickey().export_key().decode()
    return private_pem, public_pem

