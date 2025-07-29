from django.contrib import admin
from .models import VoterDB, VoteDB, Authorization
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import CommitteeMember
from django.http import HttpResponse
import base64
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import CommitteeMember 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from .forms import AuthorizationSignatureForm


admin.site.register(VoterDB)
admin.site.register(CommitteeMember)

@admin.register(Authorization)
class AuthorizationAdmin(admin.ModelAdmin):
    form = AuthorizationSignatureForm
    
    list_display = ['username', 'challenge', 'signature']


    

from django.contrib import admin, messages
from .models import VoteDB, Authorization
from .utils.crypto import reconstruct_aes_key, decrypt_vote

from .utils.crypto import decrypt_vote
from .utils.signature import verify_signature
from .forms import CommitteeSignatureForm
# vote/admin.py

from django.contrib import admin
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import VoteDB, Authorization
from vote.utils.crypto import reconstruct_aes_key, decrypt_vote
from Crypto.Cipher import AES


class VoteDBAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'timestamp')
    list_display_links = ('challenge',)
    change_list_template = "admin/vote/votedb/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('results/', self.admin_site.admin_view(self.vote_results_view), name='vote_results'),
        ]
        return custom_urls + urls
    print("🔧 vote_results_view() was triggered")

    def vote_results_view(self, request):
        results = {}

        for vote in VoteDB.objects.all():
            print(f"Checking vote with challenge: {vote.challenge}")
            auths = Authorization.objects.filter(challenge=vote.challenge)
            print(f"Signatures found: {auths.count()} for vote {vote.challenge}")

            # Filter valid authorizations with verified signatures
            valid_auths = []
            for auth in auths:
                if verify_signature(auth.username, vote.challenge, auth.signature):
                    valid_auths.append(auth)

            if len(valid_auths) < 3:
                print(f"Not enough valid signatures for vote {vote.challenge}")
                continue

            # Extract the shares from valid authorizations
            shares = [auth.share for auth in valid_auths[:3]]  # take first 3 valid shares
            print(f"Signatures used for reconstruction: {shares}")

            try:
                aes_key_hex = reconstruct_aes_key(shares)  # reconstruct AES key from shares
                plaintext = decrypt_vote(vote.encrypted_vote, aes_key_hex, vote.iv)
                results[plaintext] = results.get(plaintext, 0) + 1
            except Exception as e:
                print(f"Decryption failed for vote {vote.challenge}: {e}")
                continue

        return TemplateResponse(request, "admin/vote_results.html", {
            'title': "Election Results",
            'results': results
        })






admin.site.register(VoteDB, VoteDBAdmin)





# Add custom admin view to AdminSite

