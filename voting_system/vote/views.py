from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.base import ContentFile
from .models import VoterDB, VoteDB
import base64
import numpy as np
import face_recognition
from io import BytesIO
from PIL import Image
import cv2
import io
import logging
import json
from collections import Counter
from django.db.models import Count
from django.contrib import messages
from .models import CommitteeMember
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# Setup logger
logger = logging.getLogger(__name__)


def homepage(request):
    return render(request, 'vote/homepage.html')


def regulations(request):
    return render(request, 'vote/regulations.html')

def voting_page(request):
    return render(request, 'vote/voting.html') 



    


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')

        try:
            voter = VoterDB.objects.get(id_number=id_number)

            if not check_password(password, voter.password):
                return JsonResponse({"success": False, "error": "Invalid credentials"})

            if voter.has_voted:
                return JsonResponse({"success": False, "error": "You have already voted."})

            request.session['voter_id'] = voter.id_number
            print("Logged in voter ID saved in session:", request.session['voter_id'])  # Debug

            return JsonResponse({"success": True})

        except VoterDB.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid credentials"})

    

    return render(request, 'vote/login.html')


@csrf_exempt
def submit_vote(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            candidate = data.get("candidate")

            if not candidate:
                return JsonResponse({"success": False, "error": "No candidate selected."}, status=400)

            # Get the voter ID from the session
            voter_id = request.session.get('voter_id')
            if not voter_id:
                return JsonResponse({"success": False, "error": "Voter not found in session."}, status=403)

            try:
                voter = VoterDB.objects.get(id_number=voter_id)
            except VoterDB.DoesNotExist:
                return JsonResponse({"success": False, "error": "Voter not found."}, status=404)

            if voter.has_voted:
                return JsonResponse({"success": False, "error": "You have already voted."}, status=403)

            # Save vote
            vote = VoteDB(candidate=candidate)
            vote.save()

            # Mark voter as having voted
            voter.has_voted = True
            voter.save()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

    

@csrf_exempt
def register_page(request):
    if request.method == 'POST':
        try:
            id_number = request.POST.get('id_number')
            password = request.POST.get('password')
            face_image_data = request.POST.get('face_image')  # FIXED: use get() not get[]

            print("ID:", id_number)
            print("Password:", password)
            print("Face Image (first 30 chars):", face_image_data[:30] if face_image_data else "No image received")


            if not id_number or not password or not face_image_data:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Check if the ID number already exists
            if VoterDB.objects.filter(id_number=id_number).exists():
                return JsonResponse({'error': 'ID number already exists.'}, status=400)

            # Decode base64 face image
            format, imgstr = face_image_data.split(';base64,')  # split the metadata
            ext = format.split('/')[-1]
            image_data = base64.b64decode(imgstr)
            image_file = ContentFile(image_data, name=f'{id_number}.{ext}')  # create file for ImageField

            # Save the voter
            voter = VoterDB.objects.create(
                id_number=id_number,
                password=make_password(password),
                face_image=image_file,
                has_voted=False
            )

            return JsonResponse({'success': 'Registration successful.'})

        except Exception as e:
            logger.exception("Error in registration:")
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'vote/register.html')

from django.http import JsonResponse
from .models import VoterDB, VoteDB, Authorization
from .utils.crypto import encrypt_vote, split_key_into_shares

def cast_vote(request):
    if request.method == 'POST':
        # ✅ Get voter ID from session
        voter_id = request.session.get('voter_id')
        candidate = request.POST.get('candidate')

        if not voter_id:
            return JsonResponse({'success': False, 'error': 'Voter not found in session'})

        try:
            voter = VoterDB.objects.get(id_number=voter_id)
        except VoterDB.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Voter not found'})

        # ✅ Prevent double voting
        if voter.has_voted:
            return JsonResponse({'success': False, 'error': 'You have already voted.'})

        # 🔐 Encrypt the vote
        result = encrypt_vote(candidate)
        encrypted_vote = result['ciphertext_b64']
        iv = result['iv_b64']
        key_hex = result['key_hex']

        

        # ✅ Store the encrypted vote (no voter reference — anonymous)
        vote = VoteDB.objects.create(
            encrypted_vote=encrypted_vote,
            iv=iv,
            
        )

        # 🔐 Split AES key into shares
        shares = split_key_into_shares(key_hex, threshold=3, total=5)


        # ✅ Assign shares to committee members (first 3 as example)
        for i, share in enumerate(shares[:3]):
            Authorization.objects.create(
                challenge=vote.challenge,  # unique challenge per vote
                username=f"member{i+1}",  # must match the known usernames
                share=share,              # store the actual share here
                signature="(pending)"     # to be updated later when member signs
            )

        # ✅ Mark voter as voted (enforces one vote)
        voter.has_voted = True
        voter.save()

        return JsonResponse({'success': True, 'vote_id': vote.challenge})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



    
def live_results(request):
        votes = VoteDB.objects.values_list('candidate', flat=True)
        counts = dict(Counter(votes))
        return JsonResponse(counts)

def results_view(request):
    return render(request, 'vote/results.html')

def get_vote_counts(request):
    vote_counts = (
        VoteDB.objects.values('candidate')
        .annotate(count=Count('candidate'))
        .order_by('-count')
    )
    return JsonResponse(list(vote_counts), safe=False)

import rsa
from django.contrib import messages
from django.shortcuts import render, redirect
from vote.models import CommitteeMember
from vote.forms import CommitteeMemberLoginForm

def check_all_logged_in(request):
    # Check if all committee members are logged in by checking session data
    if all(
        request.session.get(f"committee_member_{username}") for username in ["member1", "member2", "member3"]
    ):
        # If all members are logged in, allow access to the admin page
        return redirect('admin:index')  # Redirect to the actual Django admin page
    else:
        # If not all members are logged in, redirect to the committee login page
        messages.info(request, "Please log in as all committee members.")
        return redirect('committee_login')  

# vote/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from vote.models import CommitteeMember
from vote.forms import CommitteeMemberLoginForm
from vote.utils.keys import generate_deterministic_key_pair

from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CommitteeMember
from .forms import CommitteeMemberLoginForm
from .utils.keys import generate_deterministic_key_pair  # Ensure this is your keygen function

def committee_login(request):
    # If all committee members are logged in, redirect to admin
    if all(request.session.get(f"committee_member_{u}") for u in ["member1", "member2", "member3"]):
        return redirect('admin:index')

    if request.method == 'POST':
        form = CommitteeMemberLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                member = CommitteeMember.objects.get(username=username)

                # ✅ Check if provided password matches stored hashed password
                if not check_password(password, member.password_hash):
                    messages.error(request, "❌ Incorrect password.")
                    return render(request, 'vote/committee_login.html', {'form': form})

                # ✅ Generate public key from credentials
                _, regenerated_public_pem = generate_deterministic_key_pair(username, password)

                # ✅ Compare regenerated public key with stored one
                if member.public_key.strip() == regenerated_public_pem.strip():
                    session_key = f"committee_member_{username}"
                    
                    if not request.session.get(session_key):
                        request.session[session_key] = True

                        # Count how many have logged in so far
                        logged_in_count = sum(
                            1 for u in ["member1", "member2", "member3"]
                            if request.session.get(f"committee_member_{u}")
                        )

                        messages.success(
                            request,
                            f"✅ Login successful for {username}. ({logged_in_count}/3 members logged in)"
                        )
                    else:
                        messages.info(request, f"✅ {username} is already logged in.")

                    # Redirect to admin if all 3 are in
                    if all(request.session.get(f"committee_member_{u}") for u in ["member1", "member2", "member3"]):
                        return redirect('admin:index')
                    else:
                        messages.info(request, "⏳ Waiting for other committee members.")
                else:
                    messages.error(request, "❌ Invalid credentials. Key mismatch.")

            except CommitteeMember.DoesNotExist:
                messages.error(request, "❌ Invalid username.")
            except Exception as e:
                messages.error(request, f"⚠️ An error occurred: {e}")
    else:
        form = CommitteeMemberLoginForm()

    return render(request, 'vote/committee_login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CommitteeMemberRegistrationForm
from .models import CommitteeMember
from .utils.keys import generate_deterministic_key_pair
from django.db.models import Count

def committee_register(request):
    # Count existing committee members
    member_count = CommitteeMember.objects.count()

    if member_count >= 3:
        messages.error(request, "❌ Registration closed. Three committee members have already been registered.")
        return redirect('committee_login')

    if request.method == 'POST':
        form = CommitteeMemberRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if username already exists
            if CommitteeMember.objects.filter(username=username).exists():
                messages.error(request, "❌ Username already taken.")
            else:
                # Generate keys
                _, public_pem = generate_deterministic_key_pair(username, password)
                hashed_password = make_password(password)

                # Save new member
                CommitteeMember.objects.create(
                    username=username,
                    password_hash=hashed_password,
                    public_key=public_pem
                )

                member_count += 1
                messages.success(
                    request,
                    f"✅ {username} registered successfully. ({member_count}/3 members registered)"
                )

                if member_count == 3:
                    messages.info(request, "🎉 All 3 committee members are now registered. You may proceed to login.")
                    return redirect('committee_login')
                else:
                    return redirect('committee_register')
    else:
        form = CommitteeMemberRegistrationForm()

    return render(request, 'vote/committee_register.html', {'form': form})










