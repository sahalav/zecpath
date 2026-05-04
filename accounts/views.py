from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from services.auth_service import create_user

from .models import CandidateProfile, User
from .serializers import (
    SignupSerializer,
    CandidateProfileSerializer,
    UserListSerializer
)
from .permissions import IsAdmin, IsEmployer, IsCandidate


# -------------------------
# Signup API
# -------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User created successfully"
        })

    return Response(serializer.errors)
class SignupView(APIView):
    def post(self, request):
        user = create_user(request.data)
        return Response({"message": "User created"})


# -------------------------
# Protected Profile API
# -------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "message": "Protected route success",
        "user": request.user.email
    })


# -------------------------
# Protected Views
# -------------------------
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Welcome Sahala, protected API working"
        })


class AdminView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "message": "Welcome Admin, full access granted"
        })


class EmployerView(APIView):
    permission_classes = [IsEmployer]

    def get(self, request):
        return Response({
            "message": "Employer can post jobs"
        })


class CandidateView(APIView):
    permission_classes = [IsCandidate]

    def get(self, request):
        return Response({
            "message": "Candidate can apply jobs"
        })


# -------------------------
# Candidate Profile CRUD
# -------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_candidate_profile(request):
    profile, created = CandidateProfile.objects.get_or_create(
        user=request.user
    )

    serializer = CandidateProfileSerializer(
        profile,
        data=request.data
    )

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_candidate_profile(request):
    profile = CandidateProfile.objects.get(user=request.user)
    serializer = CandidateProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_candidate_profile(request):
    profile = CandidateProfile.objects.get(user=request.user)

    serializer = CandidateProfileSerializer(
        profile,
        data=request.data
    )

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_candidate_profile(request):
    profile = CandidateProfile.objects.get(user=request.user)
    profile.is_deleted = True
    profile.save()

    return Response({
        "message": "Profile soft deleted"
    })


# -------------------------
# Resume Upload API
# -------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_resume(request):
    try:
        profile = CandidateProfile.objects.get(user=request.user)

    except CandidateProfile.DoesNotExist:
        return Response({
            "error": "Create candidate profile first"
        }, status=404)

    file = request.FILES.get('resume')

    if not file:
        return Response({
            "error": "No file uploaded"
        }, status=400)

    allowed = ['pdf', 'doc', 'docx']
    ext = file.name.split('.')[-1].lower()

    if ext not in allowed:
        return Response({
            "error": "Only PDF, DOC, DOCX allowed"
        }, status=400)

    if file.size > 5 * 1024 * 1024:
        return Response({
            "error": "File too large (max 5MB)"
        }, status=400)

    profile.resume = file
    profile.save()

    return Response({
        "message": "Resume uploaded successfully",
        "file": profile.resume.url
    })


# -------------------------
# Day 14 - Pagination / Filter / Search
# -------------------------
class UserListView(ListAPIView):

    queryset = User.objects.only(
        'id',
        'email',
        'role',
        'phone',
        'is_verified'
    ).order_by('id')

    serializer_class = UserListSerializer

    filterset_fields = ['role', 'is_verified']
    search_fields = ['email']
    ordering_fields = ['id', 'email']