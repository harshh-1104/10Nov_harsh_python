from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from allauth.account.utils import perform_login
from django.contrib import messages

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider, 
        but before the login is actually processed.
        We use this to connect existing users to their social accounts 
        automatically if the email matches.
        """
        # Social account doesn't exist yet, check if a local user exists with the same email
        if sociallogin.is_existing:
            return

        if not sociallogin.email_addresses:
            return

        email = sociallogin.email_addresses[0].email
        try:
            user = User.objects.get(email=email)
            # Link the social account to the existing user
            sociallogin.connect(request, user)
            # Optional: Add a message
            # messages.info(request, f"Social account connected to your existing account: {user.email}")
        except User.DoesNotExist:
            pass
