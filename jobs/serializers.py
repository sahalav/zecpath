from rest_framework import serializers
from .models import Job, Application,SavedJob


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['employer']

class ApplicationSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(
        source='job.title',
        read_only=True
    )

    company = serializers.CharField(
        source='job.company',
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            'id',
            'job_title',
            'company',
            'status',
            'applied_date'
        ]
class SavedJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedJob
        fields = '__all__'