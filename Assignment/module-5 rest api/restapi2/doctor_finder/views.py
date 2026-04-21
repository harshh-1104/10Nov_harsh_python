"""
API Views for the Doctor Finder app.
──────────────────────────────────────────────
Contains class-based views for:
  - Doctor CRUD (List, Create, Retrieve, Update, Delete)
  - User Registration & Login (Token Auth)
  - OTP Generation & Verification (Mock)
  - External API integrations (Jokes, Weather, GitHub, Country)

"""
import random
import string
import requests as http_requests   # renamed to avoid clash with DRF 'request'

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import generics, status, filters
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor, OTPVerification
from .serializers import (
    DoctorSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    OTPRequestSerializer,
    OTPVerifySerializer,
)


# ═══════════════════════════════════════════════
#  1. DOCTOR CRUD  (Class-Based Generic Views)
# ═══════════════════════════════════════════════

class DoctorListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/doctors/       → List all doctors (paginated)
    POST /api/doctors/       → Create a new doctor

    Supports search by name or specialty via ?search=...
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'specialty']       # ?search=cardio
    ordering_fields = ['name', 'created_at']    # ?ordering=-name


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/doctors/<id>/  → Retrieve a single doctor
    PUT    /api/doctors/<id>/  → Full update
    PATCH  /api/doctors/<id>/  → Partial update
    DELETE /api/doctors/<id>/  → Delete doctor
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


# ═══════════════════════════════════════════════
#  2. AUTHENTICATION  (Token-Based)
# ═══════════════════════════════════════════════

class RegisterView(APIView):
    """
    POST /api/register/
    Create a new user and return an auth token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create a token for the new user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Registration successful!',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'token': token.key,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /api/login/
    Authenticate user and return token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Login successful!',
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                    },
                })
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    """
    GET /api/protected/
    Example endpoint that requires a valid token.
    Demonstrates token authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': f'Hello, {request.user.username}! You are authenticated.',
            'user_id': request.user.id,
        })


# ═══════════════════════════════════════════════
#  3. OTP VERIFICATION  (Gmail SMTP)
# ═══════════════════════════════════════════════

class OTPRequestView(APIView):
    """
    POST /api/otp/request/
    Generate a 6-digit OTP and send it to the user's email via Gmail SMTP.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            # Generate a random 6-digit OTP
            otp_code = ''.join(random.choices(string.digits, k=6))
            # Store it in the database
            OTPVerification.objects.create(email=email, otp_code=otp_code)

            # Build professional HTML email
            html_content = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin:0; padding:0; background-color:#f4f7fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f7fa; padding:40px 20px;">
                    <tr>
                        <td align="center">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px; background-color:#ffffff; border-radius:16px; overflow:hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08);">

                                <!-- Header -->
                                <tr>
                                    <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:36px 40px; text-align:center;">
                                        <div style="font-size:36px; margin-bottom:8px;">🩺</div>
                                        <h1 style="color:#ffffff; font-size:22px; margin:0; font-weight:700; letter-spacing:-0.5px;">Doctor Finder</h1>
                                        <p style="color:rgba(255,255,255,0.85); font-size:13px; margin:6px 0 0;">Secure OTP Verification</p>
                                    </td>
                                </tr>

                                <!-- Body -->
                                <tr>
                                    <td style="padding:36px 40px 24px;">
                                        <p style="color:#1a1a2e; font-size:16px; margin:0 0 8px; font-weight:600;">Hello! 👋</p>
                                        <p style="color:#555; font-size:14px; line-height:1.6; margin:0 0 28px;">
                                            You requested a one-time verification code for your Doctor Finder account. Use the code below to complete your verification:
                                        </p>

                                        <!-- OTP Box -->
                                        <div style="background: linear-gradient(135deg, #f8f9ff 0%, #eef1ff 100%); border:2px dashed #667eea; border-radius:12px; padding:24px; text-align:center; margin:0 0 28px;">
                                            <p style="color:#888; font-size:11px; text-transform:uppercase; letter-spacing:2px; margin:0 0 8px; font-weight:600;">Your Verification Code</p>
                                            <p style="color:#1a1a2e; font-size:36px; font-weight:800; letter-spacing:8px; margin:0; font-family: 'Courier New', monospace;">{otp_code}</p>
                                        </div>

                                        <p style="color:#888; font-size:13px; line-height:1.5; margin:0 0 20px;">
                                            ⏱️ This code expires in <strong style="color:#667eea;">10 minutes</strong>. If you didn't request this, you can safely ignore this email.
                                        </p>
                                    </td>
                                </tr>

                                <!-- Security Tips -->
                                <tr>
                                    <td style="padding:0 40px 32px;">
                                        <div style="background-color:#fff8f0; border-left:4px solid #f59e0b; border-radius:0 8px 8px 0; padding:14px 18px;">
                                            <p style="color:#92400e; font-size:12px; margin:0; font-weight:600;">🔒 Security Tip</p>
                                            <p style="color:#78350f; font-size:12px; margin:4px 0 0; line-height:1.5;">Never share this code with anyone. Doctor Finder staff will never ask for your OTP.</p>
                                        </div>
                                    </td>
                                </tr>

                                <!-- Footer -->
                                <tr>
                                    <td style="background-color:#f8f9fa; padding:24px 40px; border-top:1px solid #eee; text-align:center;">
                                        <p style="color:#aaa; font-size:11px; margin:0 0 4px;">
                                            Sent by Doctor Finder REST API &middot; Module 5 Assignment
                                        </p>
                                        <p style="color:#ccc; font-size:11px; margin:0;">
                                            Built with Django + DRF &middot; &copy; 2026
                                        </p>
                                    </td>
                                </tr>

                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            '''

            plain_text = f'Your Doctor Finder OTP code is: {otp_code}\n\nThis code expires in 10 minutes. Do not share it with anyone.'

            # Send OTP via Gmail SMTP
            from django.core.mail import EmailMultiAlternatives
            try:
                msg = EmailMultiAlternatives(
                    subject='🔐 Your Doctor Finder OTP Code',
                    body=plain_text,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)

                return Response({
                    'message': f'OTP sent to {email}',
                    'otp_code': otp_code,   # Shown for demo purposes only!
                })
            except Exception as e:
                # Email failed but OTP is still in DB — return it for demo
                print(f"\n⚠️ Email send failed: {e}\n")
                return Response({
                    'message': f'OTP generated (email delivery failed — check Gmail App Password)',
                    'otp_code': otp_code,
                    'email_error': str(e),
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    """
    POST /api/otp/verify/
    Verify the OTP code for a given email.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            try:
                otp_obj = OTPVerification.objects.filter(
                    email=email, otp_code=otp_code, is_verified=False
                ).latest('created_at')
                otp_obj.is_verified = True
                otp_obj.save()
                return Response({'message': 'OTP verified successfully! ✓'})
            except OTPVerification.DoesNotExist:
                return Response(
                    {'error': 'Invalid or expired OTP'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ═══════════════════════════════════════════════
#  4. EXTERNAL API INTEGRATIONS
# ═══════════════════════════════════════════════

class RandomJokeView(APIView):
    """
    GET /api/joke/
    Fetch a random joke from the JokeAPI.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            response = http_requests.get(
                'https://v2.jokeapi.dev/joke/Any?type=single',
                timeout=5,
            )
            data = response.json()
            if data.get('error'):
                return Response({'joke': 'Why did the API fail? Because it had no sense of humor!'})
            return Response({
                'category': data.get('category', 'Unknown'),
                'joke': data.get('joke', 'No joke found'),
            })
        except Exception as e:
            return Response({
                'joke': 'Could not fetch joke. Here is one: Why do programmers prefer dark mode? Because light attracts bugs!',
                'error': str(e),
            })


class WeatherView(APIView):
    """
    GET /api/weather/?city=London
    Fetch current weather from OpenWeatherMap.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city', 'London')
        api_key = settings.OPENWEATHERMAP_API_KEY

        if not api_key:
            # Return mock data if no API key is configured
            return Response({
                'city': city,
                'temperature': '25°C',
                'description': 'Sunny (Mock Data — set OPENWEATHERMAP_API_KEY for real data)',
                'humidity': '60%',
                'mock': True,
            })

        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            response = http_requests.get(url, timeout=5)
            data = response.json()

            if data.get('cod') != 200:
                return Response({'error': data.get('message', 'City not found')},
                                status=status.HTTP_404_NOT_FOUND)

            return Response({
                'city': data['name'],
                'temperature': f"{data['main']['temp']}°C",
                'description': data['weather'][0]['description'].title(),
                'humidity': f"{data['main']['humidity']}%",
                'wind_speed': f"{data['wind']['speed']} m/s",
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GitHubReposView(APIView):
    """
    GET /api/github/?username=octocat
    List public repositories for a GitHub user.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get('username', 'octocat')
        try:
            headers = {}
            if settings.GITHUB_TOKEN:
                headers['Authorization'] = f'token {settings.GITHUB_TOKEN}'

            response = http_requests.get(
                f'https://api.github.com/users/{username}/repos?sort=updated&per_page=10',
                headers=headers,
                timeout=5,
            )
            if response.status_code == 404:
                return Response({'error': f'User "{username}" not found'},
                                status=status.HTTP_404_NOT_FOUND)

            repos = response.json()
            return Response({
                'username': username,
                'repo_count': len(repos),
                'repositories': [
                    {
                        'name': repo['name'],
                        'description': repo.get('description', ''),
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count'],
                        'language': repo.get('language', 'N/A'),
                    }
                    for repo in repos
                ],
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CountryInfoView(APIView):
    """
    GET /api/country/?name=India
    Fetch country info (population, languages, currency).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        country_name = request.query_params.get('name', 'India')
        try:
            response = http_requests.get(
                f'https://restcountries.com/v3.1/name/{country_name}',
                timeout=5,
            )
            if response.status_code == 404:
                return Response({'error': f'Country "{country_name}" not found'},
                                status=status.HTTP_404_NOT_FOUND)

            data = response.json()[0]
            currencies = data.get('currencies', {})
            currency_info = []
            for code, info in currencies.items():
                currency_info.append(f"{info['name']} ({info.get('symbol', code)})")

            languages = list(data.get('languages', {}).values())

            return Response({
                'name': data.get('name', {}).get('common', country_name),
                'official_name': data.get('name', {}).get('official', ''),
                'capital': data.get('capital', ['N/A'])[0],
                'population': f"{data.get('population', 0):,}",
                'region': data.get('region', 'N/A'),
                'languages': languages,
                'currencies': currency_info,
                'flag': data.get('flags', {}).get('svg', ''),
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# ═══════════════════════════════════════════════
#  5. DASHBOARD STATS
# ═══════════════════════════════════════════════

class DashboardStatsView(APIView):
    """
    GET /api/stats/
    Returns quick stats for the dashboard.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        total_doctors = Doctor.objects.count()
        specialties = Doctor.objects.values_list('specialty', flat=True).distinct().count()
        total_users = User.objects.count()
        latest_doctor = Doctor.objects.first()  # ordered by -created_at

        return Response({
            'total_doctors': total_doctors,
            'total_specialties': specialties,
            'total_users': total_users,
            'latest_doctor': DoctorSerializer(latest_doctor).data if latest_doctor else None,
        })
