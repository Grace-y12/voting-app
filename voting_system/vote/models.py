from django.db import models
import uuid

class VoterDB(models.Model):
    
    id_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length= 10)
    face_image = models.ImageField(upload_to="face_images/")
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return f"  ({self.id_number})"


class VoteDB(models.Model):
    challenge = models.AutoField(primary_key=True)  # Sequential ID
    encrypted_vote = models.TextField()
    iv = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote {self.challenge} at {self.timestamp}"


class Authorization(models.Model):
    challenge = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    signature = models.TextField()
    share = models.CharField(max_length=200)

    def __str__(self):
        return f"Authorization by {self.username} for challenge {self.challenge}"

    
class CommitteeMember(models.Model):
    username = models.CharField(max_length=150)
    password_hash = models.CharField(max_length=255)
    public_key = models.TextField()  # Store public key in PEM format

    def __str__(self):
        return self.username
# Create your models here.
