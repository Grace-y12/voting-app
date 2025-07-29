

from django.core.management.base import BaseCommand
from vote.models import CommitteeMember
from vote.utils.keys import generate_deterministic_key_pair

class Command(BaseCommand):
    help = 'Regenerates and updates the public keys for all committee members.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🔁 Starting public key regeneration...'))

        for member in CommitteeMember.objects.all():
            username = member.username
            password = input(f"🔐 Enter password for '{username}': ").strip()

            try:
                _, public_pem = generate_deterministic_key_pair(username, password)
                member.public_key = public_pem
                member.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Public key updated for {username}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Failed for {username}: {e}"))

        self.stdout.write(self.style.SUCCESS('🎉 Public key regeneration complete!'))
