from django.db import models

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)

    skills = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    salary = models.IntegerField()
    experience = models.IntegerField()

    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title