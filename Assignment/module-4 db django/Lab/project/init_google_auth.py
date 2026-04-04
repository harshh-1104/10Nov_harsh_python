import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def init_google_auth():
    # 1. Update Site name/domain if necessary (default is example.com)
    site = Site.objects.get_or_create(id=1)[0]
    site.domain = '127.0.0.1:8000'
    site.name = 'Finance Tracker'
    site.save()
    
    print(f"Updated Site: {site.domain}")

    # 2. Create SocialApp for Google
    client_id = input("Enter your Google Client ID: ").strip()
    client_secret = input("Enter your Google Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("Error: Client ID and Secret are required.")
        return

    app, created = SocialApp.objects.get_or_create(
        provider='google',
        name='Google Auth'
    )
    app.client_id = client_id
    app.secret = client_secret
    app.sites.add(site)
    app.save()
    
    if created:
        print("Successfully created Google SocialApp.")
    else:
        print("Successfully updated Google SocialApp.")

if __name__ == "__main__":
    init_google_auth()
