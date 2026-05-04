# services/auth_service.py

from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(data):
    return User.objects.create_user(
        email=data['email'],
        password=data['password'],
        role=data['role']
    )