from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CandidateProfile, EmployerProfile
from .models import User
from .models import Resume

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user


class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = '__all__'
        read_only_fields = ['user', 'is_deleted']


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = '__all__'
        read_only_fields = ['user', 'is_deleted']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone', 'is_verified']


class ResumeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Resume

        fields = '__all__'
