from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# ✅ 1. Job List API
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer


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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ 3. Test API
class TestAPI(APIView):
    def get(self, request):
        return Response({"message": "Hello Sahala 😊"})
class JobUpdateAPI(APIView):
    def put(self, request, id):
        try:
            job = Job.objects.get(id=id)
        except Job.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        serializer = JobSerializer(job, data=request.data)
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
