from rest_framework import serializers
from .models import Job, Application, SavedJob
from datetime import datetime


from django.utils import timezone


from .models import InterviewRescheduleRequest


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
class InterviewRescheduleRequestSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = InterviewRescheduleRequest

        fields = [
            "id",
            "interview",
            "requested_by",
            "old_date",
            "old_time",
            "new_date",
            "new_time",
            "reason",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
    "id",
    "interview",
    "requested_by",
    "old_date",
    "old_time",
    "status",
    "created_at",
    "updated_at",
]
    def validate(self, attrs):

        new_date = attrs.get("new_date")
        new_time = attrs.get("new_time")

        requested_datetime = timezone.make_aware(
            datetime.combine(
                new_date,
                new_time
            )
        )

        if requested_datetime <= timezone.now():
            raise serializers.ValidationError(
                "Interview date and time must be in the future."
            )

        interview = self.context.get("interview")

        if interview:
            if (
                new_date == interview.interview_date
                and new_time == interview.interview_time
            ):
                raise serializers.ValidationError(
                    "New date and time must be different "
                    "from the current interview schedule."
                )

        return attrs