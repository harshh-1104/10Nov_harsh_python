"""
Serializers for the Doctor Finder app.
──────────────────────────────────────────────
Converts Doctor model instances ↔ JSON for the REST API.
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Doctor, OTPVerification


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Doctor model.

    Converts Doctor objects to/from JSON.
    All fields are included; 'id', 'created_at', 'updated_at' are read-only.
    """

    class Meta:
        model = Doctor
        fields = '__all__'                     # Include every field
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Accepts username, email, password and creates a new Django user.
    Password is write-only (never returned in responses).
    """
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        """Create a new user with hashed password."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Accepts username + password, validates credentials.
    """
    username = serializers.CharField()
    password = serializers.CharField()


class OTPRequestSerializer(serializers.Serializer):
    """Accepts an email to send OTP to."""
    email = serializers.EmailField()


class OTPVerifySerializer(serializers.Serializer):
    """Accepts email + OTP code for verification."""
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
