import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voting_system.settings")  # replace with your project name
django.setup()

from vote.models import CommitteeMember
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

def generate_member_keys(member_name):
    # Generate private/public key pair
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Serialize public key to PEM format
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    # Store in database
    member, created = CommitteeMember.objects.get_or_create(name=member_name)
    member.public_key = pem_public
    member.save()

    # Sign a fixed access request message
    message = b"ACCESS_REQUEST"
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    signature_b64 = base64.b64encode(signature).decode()

    print(f"\n✅ Member: {member_name}")
    print("Public Key saved to DB.")
    print("Signature for ACCESS_REQUEST (Base64):")
    print(signature_b64)

# Generate for 3 committee members
generate_member_keys("committee1")
generate_member_keys("committee2")
generate_member_keys("committee3")
