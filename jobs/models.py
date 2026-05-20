from django.db import models
from accounts.models import User


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

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    employer = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={'role': 'employer'}
)

    def __str__(self):
        return self.title


class Application(models.Model):

    STATUS_CHOICES = (
    ('applied', 'Applied'),
    ('shortlisted', 'Shortlisted'),
    ('interview', 'Interview Scheduled'),
    ('selected', 'Selected'),
    ('rejected', 'Rejected'),
)

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied'
    )

    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.email} - {self.job.title}"
class SavedJob(models.Model):

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.candidate.email} saved {self.job.title}"
class AuditLog(models.Model):

    ACTION_CHOICES = (
        ('approve_employer', 'Approve Employer'),
        ('block_user', 'Block User'),
        ('delete_job', 'Delete Job'),
        ('update_status', 'Update Status'),
    )

    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES
    )

    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='target_user'
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.admin.email} - {self.action}"
class ATSScore(models.Model):

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    score = models.FloatField()

    status = models.CharField(
        max_length=50,
        default='pending'
    )