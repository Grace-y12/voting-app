import os
import django
import rsa
from django.contrib.auth.hashers import make_password
import hashlib

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voting_system.settings")  # change if needed
django.setup()

from vote.models import CommitteeMember

# Create the keys directory if it doesn't exist
KEYS_DIR = "keys"
os.makedirs(KEYS_DIR, exist_ok=True)

def create_member(username, password):
    if CommitteeMember.objects.filter(username=username).exists():
        print(f"⚠️  Username '{username}' already exists. Skipping.")
        return

    public_key, private_key = rsa.newkeys(512)
    public_key_pem = public_key.save_pkcs1().decode()
    private_key_pem = private_key.save_pkcs1().decode()
    hashed_password = make_password(password)

    # Create member in database
    CommitteeMember.objects.create(
        username=username,
        hashed_password=hashed_password,
        public_key=public_key_pem
    )

    # Save private key in the keys directory
    filename = os.path.join(KEYS_DIR, f"{username}_private_key.pem")
    with open(filename, "w") as f:
        f.write(private_key_pem)

    print(f"\n✅ Created: {username}")
    print(f"🔑 Password: {hashed_password}")
    print(f"📄 Private key saved to: {filename}")
    print("=" * 60)

# Create 3 members
create_member("member1", "pass123")
create_member("member2", "pass456")
create_member("member3", "pass789")
