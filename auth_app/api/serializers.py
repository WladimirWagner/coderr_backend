from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Handles user registration with password validation and email uniqueness check.
    Creates a new user with the provided credentials.
    """
    repeated_password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'Email is already in use.'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'error': 'Username is already in use.'})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Handles user authentication with username and password.
    Validates credentials and returns user object if successful.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username:
            raise serializers.ValidationError({'error': 'Username is required.'})

        if not password:
            raise serializers.ValidationError({'error': 'Password is required.'})

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError({'error': 'Invalid credentials.'})

        data['user'] = user
        return data
