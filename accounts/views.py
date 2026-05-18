from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication
import PyPDF2
import pdfplumber
import docx

from io import BytesIO
from services.auth_service import create_user

from .models import CandidateProfile, User, Resume
from .serializers import (
    SignupSerializer,
    CandidateProfileSerializer,
    UserListSerializer
)

from .permissions import (
    IsAdmin,
    IsEmployer,
    IsCandidate
)


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

        return Response({
            "message": "User created"
        })


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
            "message": "Protected API working"
        })


class AdminView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        return Response({
            "message": "Welcome Admin"
        })


class EmployerView(APIView):

    permission_classes = [IsEmployer]

    def get(self, request):

        return Response({
            "message": "Employer access granted"
        })


class CandidateView(APIView):

    permission_classes = [IsCandidate]

    def get(self, request):

        return Response({
            "message": "Candidate access granted"
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

    profile = CandidateProfile.objects.get(
        user=request.user
    )

    serializer = CandidateProfileSerializer(profile)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_candidate_profile(request):

    profile = CandidateProfile.objects.get(
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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_candidate_profile(request):

    profile = CandidateProfile.objects.get(
        user=request.user
    )

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
        profile = CandidateProfile.objects.get(
            user=request.user
        )

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
# User List API
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


# -------------------------
# Approve Employer API
# -------------------------
class ApproveEmployerAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):

        if not request.user.is_superuser:

            return Response({
                "error": "Admin only"
            }, status=403)

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:

            return Response({
                "error": "User not found"
            }, status=404)

        user.is_approved = True
        user.save()

        return Response({
            "message": "Employer approved"
        })


# -------------------------
# Flag User API
# -------------------------
class FlagUserAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):

        if not request.user.is_superuser:

            return Response({
                "error": "Admin only"
            }, status=403)

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:

            return Response({
                "error": "User not found"
            }, status=404)

        user.is_flagged = True
        user.save()

        return Response({
            "message": "User flagged successfully"
        })


# -------------------------
# View Flagged Users API
# -------------------------
class FlaggedUsersAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_superuser:

            return Response({
                "error": "Admin only"
            }, status=403)

        users = User.objects.filter(
            is_flagged=True
        )

        data = []

        for user in users:

            data.append({
                "id": user.id,
                "email": user.email,
                "role": user.role
            })

        return Response(data)
class ResumeParserAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        file = request.FILES.get('file')

        if not file:

            return Response({
                "error": "No file uploaded"
            }, status=400)

        extracted_text = ""

        # PDF Parsing
        if file.name.endswith('.pdf'):

            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:

                text = page.extract_text()

                if text:
                    extracted_text += text + "\n"

        # DOCX Parsing
        elif file.name.endswith('.docx'):

            document = docx.Document(file)

            for para in document.paragraphs:

                extracted_text += para.text + "\n"

        else:

            return Response({
                "error": "Only PDF and DOCX supported"
            }, status=400)

        # Cleaning
        cleaned_text = " ".join(
            extracted_text.split()
        )

        resume = Resume.objects.create(

            user=request.user,

            file=file,

            extracted_text=cleaned_text
        )

        return Response({

            "message": "Resume parsed successfully",

            "resume_id": resume.id,

            "cleaned_text": cleaned_text
        })