import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from .keys import generate_deterministic_key_pair

def sign_data(username, password, data: str) -> str:
    """
    Signs the given data using a deterministic private key.
    Returns base64-encoded signature.
    """
    private_pem, _ = generate_deterministic_key_pair(username, password)
    key = RSA.import_key(private_pem)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(key).sign(h)
    return base64.b64encode(signature).decode()

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from base64 import b64decode
from vote.models import CommitteeMember

def verify_signature(username, challenge, signature_b64):
    try:
        # Get member
        member = CommitteeMember.objects.get(username=username)
        public_key = serialization.load_pem_public_key(member.public_key.encode())

        # Decode signature
        signature = b64decode(signature_b64)

        challenge_bytes = str(challenge).encode()


        # Verify
        public_key.verify(
            signature,
            challenge_bytes,  # must be bytes
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"[❌] Signature verification failed for {username}: {e}")
        return False



