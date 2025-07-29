from django import forms

from django import forms

class CommitteeMemberRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


class CommitteeMemberLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CommitteeSignatureForm(forms.Form):
    username1 = forms.CharField(label="Username 1")
    signature1 = forms.CharField(label="Signature 1", widget=forms.Textarea)

    username2 = forms.CharField(label="Username 2")
    signature2 = forms.CharField(label="Signature 2", widget=forms.Textarea)

    username3 = forms.CharField(label="Username 3")
    signature3 = forms.CharField(label="Signature 3", widget=forms.Textarea)

# vote/forms.py
from django import forms
from .models import Authorization
from django import forms
from .models import Authorization
from vote.utils.keys import generate_deterministic_key_pair
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import base64

class AuthorizationSignatureForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        help_text="Enter your password to generate your digital signature."
    )

    class Meta:
        model = Authorization
        fields = ['username', 'challenge', 'password', 'signature']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'signature' in self.fields:
        # Make signature readonly in form display
          self.fields['signature'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        # Extract cleaned data
        username = self.cleaned_data['username']
        challenge = self.cleaned_data['challenge']
        password = self.cleaned_data['password']

        # Generate private key
        priv_pem, _ = generate_deterministic_key_pair(username, password)
        from Crypto.PublicKey import RSA
        priv_key = RSA.import_key(priv_pem)

        # Create the challenge hash
        challenge_hash = SHA256.new(challenge.encode())

        # Sign the challenge
        signature = pkcs1_15.new(priv_key).sign(challenge_hash)
        signature_b64 = base64.b64encode(signature).decode()

        # Save the signature to the instance
        self.instance.signature = signature_b64

        # Do NOT save password
        return super().save(commit=commit)
