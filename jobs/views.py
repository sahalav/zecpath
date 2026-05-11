from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# ✅ 1. Job List API
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job,Application
from .serializers import JobSerializer,ApplicationSerializer
from rest_framework.permissions import IsAuthenticated


class JobListAPI(APIView):

    def get(self, request):

        jobs = Job.objects.filter(is_active=True)

        # Featured jobs
        featured = request.GET.get('featured')

        if featured == 'true':
            jobs = jobs.filter(is_featured=True)

        # Latest jobs
        latest = request.GET.get('latest')

        if latest == 'true':
            jobs = jobs.order_by('-created_at')

        # Skill search
        skills = request.GET.get('skills')

        if skills:
            jobs = jobs.filter(skills__icontains=skills)

        # Location filter
        location = request.GET.get('location')

        if location:
            jobs = jobs.filter(location__icontains=location)

        # Salary filter
        salary = request.GET.get('salary')

        if salary:
            jobs = jobs.filter(salary__gte=salary)

        # Experience filter
        experience = request.GET.get('experience')

        if experience:
            jobs = jobs.filter(experience__gte=experience)

        # Job type filter
        job_type = request.GET.get('job_type')

        if job_type:
            jobs = jobs.filter(job_type=job_type)

        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data)

# ✅ 2. Job Create API
from rest_framework.permissions import IsAuthenticated

class JobCreateAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # ROLE CHECK
        if request.user.role != "employer":
            return Response(
                {"error": "Only employers can create jobs"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(employer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ 3. Test API
class TestAPI(APIView):
    def get(self, request):
        return Response({"message": "Hello Sahala 😊"})
class JobUpdateAPI(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, id):

        # Employer only
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

        # Ownership validation
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

        return Response(serializer.errors)
    
class JobDeleteAPI(APIView):
    def delete(self, request, id):
        try:
            job = Job.objects.get(id=id)
        except Job.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        job.delete()
        return Response({"message": "Deleted successfully"})
class ApplyJobAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):

        # Candidate only
        if request.user.role != "candidate":
            return Response(
                {"error": "Only candidates can apply"},
                status=403
            )

        # Get job
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=404
            )

        # Duplicate prevention
        already_applied = Application.objects.filter(
            candidate=request.user,
            job=job
        ).exists()

        if already_applied:
            return Response(
                {"error": "Already applied"},
                status=400
            )

        # Create application
        application = Application.objects.create(
            candidate=request.user,
            job=job
        )

        serializer = ApplicationSerializer(application)

        return Response(serializer.data, status=201)
class UpdateApplicationStatusAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, application_id):

        # Employer only
        if request.user.role != "employer":
            return Response(
                {"error": "Only employers allowed"},
                status=403
            )

        try:
            application = Application.objects.get(
                id=application_id
            )

        except Application.DoesNotExist:
            return Response(
                {"error": "Application not found"},
                status=404
            )

        new_status = request.data.get('status')

        # Workflow validation
        if application.status == 'rejected':
            return Response({
                "error": "Rejected applications cannot move further"
            })

        valid_statuses = [
            'applied',
            'shortlisted',
            'interview',
            'selected',
            'rejected'
        ]

        if new_status not in valid_statuses:
            return Response(
                {"error": "Invalid status"}
            )

        application.status = new_status
        application.save()

        return Response({
            "message": "Status updated",
            "new_status": application.status
        })
class EmployerJobsAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "employer":
            return Response({
                "error": "Only employers allowed"
            })

        jobs = Job.objects.filter(
            employer=request.user
        )

        serializer = JobSerializer(
            jobs,
            many=True
        )

        return Response(serializer.data)
class ApplicantsAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Employer only
        if request.user.role != "employer":
            return Response({
                "error": "Only employers allowed"
            }, status=403)

        applications = Application.objects.all()

        # Filter by status
        status_filter = request.GET.get('status')

        if status_filter:
            applications = applications.filter(
                status=status_filter
            )

        # Search candidate
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