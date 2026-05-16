from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import User

from .models import (
    Job,
    Application,
    SavedJob,
    AuditLog
)

from .serializers import (
    JobSerializer,
    ApplicationSerializer,
    SavedJobSerializer
)


# ✅ 1. Job List API
class JobListAPI(APIView):

    def get(self, request):

        jobs = Job.objects.filter(is_active=True)

        featured = request.GET.get('featured')

        if featured == 'true':
            jobs = jobs.filter(is_featured=True)

        latest = request.GET.get('latest')

        if latest == 'true':
            jobs = jobs.order_by('-created_at')

        skills = request.GET.get('skills')

        if skills:
            jobs = jobs.filter(skills__icontains=skills)

        location = request.GET.get('location')

        if location:
            jobs = jobs.filter(location__icontains=location)

        salary = request.GET.get('salary')

        if salary:
            jobs = jobs.filter(salary__gte=salary)

        experience = request.GET.get('experience')

        if experience:
            jobs = jobs.filter(experience__gte=experience)

        job_type = request.GET.get('job_type')

        if job_type:
            jobs = jobs.filter(job_type=job_type)

        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data)


# ✅ 2. Job Create API
class JobCreateAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != "employer":
            return Response({
                "error": "Only employers can create jobs"
            }, status=403)

        if not request.user.is_approved:
            return Response({
                "error": "Employer not approved yet"
            }, status=403)

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(employer=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)


# ✅ 3. Test API
class TestAPI(APIView):

    def get(self, request):

        return Response({
            "message": "Hello Sahala 😊"
        })


# ✅ 4. Job Update API
class JobUpdateAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):

        if request.user.role != "employer":
            return Response({
                "error": "Only employers allowed"
            }, status=403)

        try:
            job = Job.objects.get(id=id)

        except Job.DoesNotExist:
            return Response({
                "error": "Job not found"
            }, status=404)

        if job.employer != request.user:
            return Response({
                "error": "Unauthorized"
            }, status=403)

        serializer = JobSerializer(
            job,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)


# ✅ 5. Job Delete API
class JobDeleteAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        if not request.user.is_superuser:
            return Response({
                "error": "Admin only"
            }, status=403)

        try:
            job = Job.objects.get(id=id)

        except Job.DoesNotExist:
            return Response({
                "error": "Job not found"
            }, status=404)

        job.delete()

        AuditLog.objects.create(
            admin=request.user,
            action='delete_job',
            description='Admin deleted a job'
        )

        return Response({
            "message": "Job deleted successfully"
        })


# ✅ 6. Apply Job API
class ApplyJobAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):

        if request.user.role != "candidate":
            return Response({
                "error": "Only candidates can apply"
            }, status=403)

        try:
            job = Job.objects.get(id=job_id)

        except Job.DoesNotExist:
            return Response({
                "error": "Job not found"
            }, status=404)

        already_applied = Application.objects.filter(
            candidate=request.user,
            job=job
        ).exists()

        if already_applied:
            return Response({
                "error": "Already applied"
            }, status=400)

        application = Application.objects.create(
            candidate=request.user,
            job=job
        )

        serializer = ApplicationSerializer(application)

        return Response(serializer.data, status=201)


# ✅ 7. ATS Status Update API
class UpdateApplicationStatusAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, application_id):

        if request.user.role != "employer":
            return Response({
                "error": "Only employers allowed"
            }, status=403)

        try:
            application = Application.objects.get(
                id=application_id
            )

        except Application.DoesNotExist:
            return Response({
                "error": "Application not found"
            }, status=404)

        new_status = request.data.get('status')

        valid_statuses = [
            'applied',
            'shortlisted',
            'interview',
            'selected',
            'rejected'
        ]

        if new_status not in valid_statuses:
            return Response({
                "error": "Invalid status"
            }, status=400)

        if application.status == 'rejected':
            return Response({
                "error": "Rejected applications cannot move further"
            }, status=400)

        application.status = new_status
        application.save()

        return Response({
            "message": "Status updated",
            "new_status": application.status
        })


# ✅ 8. Employer Jobs API
class EmployerJobsAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "employer":
            return Response({
                "error": "Only employers allowed"
            }, status=403)

        jobs = Job.objects.filter(
            employer=request.user
        )

        serializer = JobSerializer(
            jobs,
            many=True
        )

        return Response(serializer.data)


# ✅ 9. Applicants API
class ApplicantsAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "employer":
            return Response({
                "error": "Only employers allowed"
            }, status=403)

        applications = Application.objects.all()

        status_filter = request.GET.get('status')

        if status_filter:
            applications = applications.filter(
                status=status_filter
            )

        search = request.GET.get('search')

        if search:
            applications = applications.filter(
                candidate__email__icontains=search
            )

        serializer = ApplicationSerializer(
            applications,
            many=True
        )

        return Response(serializer.data)


# ✅ 10. Applied Jobs API
class AppliedJobsAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "candidate":
            return Response({
                "error": "Only candidates allowed"
            }, status=403)

        applications = Application.objects.filter(
            candidate=request.user
        )

        serializer = ApplicationSerializer(
            applications,
            many=True
        )

        return Response(serializer.data)


# ✅ 11. Save Job API
class SaveJobAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):

        if request.user.role != "candidate":
            return Response({
                "error": "Only candidates allowed"
            }, status=403)

        try:
            job = Job.objects.get(id=job_id)

        except Job.DoesNotExist:
            return Response({
                "error": "Job not found"
            }, status=404)

        saved_job = SavedJob.objects.create(
            candidate=request.user,
            job=job
        )

        serializer = SavedJobSerializer(saved_job)

        return Response(serializer.data)


# ✅ 12. Recommendation API
class RecommendationAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "candidate":
            return Response({
                "error": "Only candidates allowed"
            }, status=403)

        jobs = Job.objects.filter(
            skills__icontains="Python"
        )

        serializer = JobSerializer(
            jobs,
            many=True
        )

        return Response(serializer.data)


# ✅ 13. Platform Stats API
class PlatformStatsAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_superuser:
            return Response({
                "error": "Admin only"
            }, status=403)

        total_users = User.objects.count()
        total_jobs = Job.objects.count()
        total_applications = Application.objects.count()

        return Response({
            "total_users": total_users,
            "total_jobs": total_jobs,
            "total_applications": total_applications
        })


# ✅ 14. Audit Log API
class AuditLogAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_superuser:
            return Response({
                "error": "Admin only"
            }, status=403)

        logs = AuditLog.objects.all().order_by(
            '-created_at'
        )

        data = []

        for log in logs:

            data.append({
                "admin": log.admin.email,
                "action": log.action,
                "description": log.description,
                "time": log.created_at
            })

        return Response(data)


# ✅ 15. Approve Employer API
class ApproveEmployerAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):

        print(request.user)
        print(request.user.is_superuser)

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

        AuditLog.objects.create(
            admin=request.user,
            action='approve_employer',
            target_user=user,
            description='Employer approved by admin'
        )

        return Response({
            "message": "Employer approved"
        })


# ✅ 16. Block User API
class BlockUserAPI(APIView):

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

        user.is_blocked = True
        user.save()

        AuditLog.objects.create(
            admin=request.user,
            action='block_user',
            target_user=user,
           description='User blocked by admin'
        )

        return Response({
            "message": "User blocked"
        })
class PlatformStatsAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_superuser:

            return Response({
                "error": "Admin only"
            }, status=403)

        total_users = User.objects.count()

        total_jobs = Job.objects.count()

        total_applications = Application.objects.count()

        total_employers = User.objects.filter(
            role='employer'
        ).count()

        total_candidates = User.objects.filter(
            role='candidate'
        ).count()

        return Response({

            "total_users": total_users,

            "total_jobs": total_jobs,

            "total_applications": total_applications,

            "total_employers": total_employers,

            "total_candidates": total_candidates
        })
class UserGrowthAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_superuser:

            return Response({
                "error": "Admin only"
            }, status=403)

        users = User.objects.order_by(
            '-date_joined'
        )[:10]

        data = []

        for user in users:

            data.append({

                "id": user.id,

                "email": user.email,

                "role": user.role,

                "joined": user.date_joined
            })

        return Response(data)
class JobActivityAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_superuser:

            return Response({
                "error": "Admin only"
            }, status=403)

        jobs = Job.objects.all()

        data = []

        for job in jobs:

            data.append({

                "id": job.id,

                "title": job.title,

                "location": job.location,

                "job_type": job.job_type,

                "is_active": job.is_active
            })

        return Response(data)