from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from .serializers import JobSerializer

# ✅ 1. Job List API
class JobListAPI(APIView):
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

# ✅ 2. Job Create API
class JobCreateAPI(APIView):
    def post(self, request):
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
