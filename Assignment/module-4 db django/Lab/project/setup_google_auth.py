import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def setup_google():
    # Credentials from environment variables (recommended)
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "YOUR_GOOGLE_OAUTH_CLIENT_ID")
    secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", "YOUR_GOOGLE_OAUTH_CLIENT_SECRET")
    
    # 1. Update Site domain
    print("For PythonAnywhere, your domain is usually 'yourusername.pythonanywhere.com'")
    domain_input = input("Enter your domain (press Enter to use 127.0.0.1:8000 for local): ").strip()
    domain = domain_input if domain_input else "127.0.0.1:8000"
    site = Site.objects.get_or_create(id=1)[0]
    site.domain = domain
    site.name = domain
    site.save()
    print(f"Site configured: {site.domain}")

    # 2. Configure SocialApp
    app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google Auth',
            'client_id': client_id,
            'secret': secret,
        }
    )
    
    if not created:
        app.client_id = client_id
        app.secret = secret
        app.save()
        print("Existing SocialApp updated.")
    else:
        print("New SocialApp created.")

    # 3. Associate Site with App
    app.sites.add(site)
    print("SocialApp associated with Site.")

if __name__ == "__main__":
    setup_google()
