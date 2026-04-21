"""
URL Configuration for the Doctor Finder app.
──────────────────────────────────────────────
Defines both API endpoints and template (UI) routes.
"""
from django.urls import path
from . import views
from . import template_views

urlpatterns = [
    # ─── UI PAGES (Templates) ──────────────────
    path('', template_views.home_view, name='home'),
    path('joke/', template_views.joke_page, name='joke_page'),
    path('setup/', template_views.setup_page, name='setup_page'),
    path('doctors-ui/', template_views.doctors_page, name='doctors_page'),
    path('auth-ui/', template_views.auth_page, name='auth_page'),
    path('weather-ui/', template_views.weather_page, name='weather_page'),
    path('github-ui/', template_views.github_page, name='github_page'),
    path('country-ui/', template_views.country_page, name='country_page'),

    path('otp-ui/', template_views.otp_page, name='otp_page'),

    # ─── API ENDPOINTS ─────────────────────────
    # Doctor CRUD
    path('api/doctors/', views.DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('api/doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),

    # Authentication
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/protected/', views.ProtectedView.as_view(), name='protected'),

    # OTP
    path('api/otp/request/', views.OTPRequestView.as_view(), name='otp-request'),
    path('api/otp/verify/', views.OTPVerifyView.as_view(), name='otp-verify'),

    # External APIs
    path('api/joke/', views.RandomJokeView.as_view(), name='random-joke'),
    path('api/weather/', views.WeatherView.as_view(), name='weather'),
    path('api/github/', views.GitHubReposView.as_view(), name='github-repos'),
    path('api/country/', views.CountryInfoView.as_view(), name='country-info'),


    # Dashboard Stats
    path('api/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
]
