from django.shortcuts import redirect
from django.urls import reverse

class CheckCommitteeLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is going to the admin page
        if request.path.startswith('/admin/'):
            # Check if all committee members are logged in
            committee_members_logged_in = all(
                request.session.get(f"committee_member_{username}") for username in ["member1", "member2", "member3"]
            )

            if not committee_members_logged_in:
                # Redirect to committee login if not all committee members are logged in
                return redirect('committee_login')
        
        # Allow the request to continue if not an admin page
        response = self.get_response(request)
        return response