from django.db import models
from accounts.models import User


class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
    )

    title = models.CharField(
    max_length=255,
    db_index=True
)
    description = models.TextField()
    company = models.CharField(max_length=255)

    skills = models.CharField(
    max_length=255,
    db_index=True
)
    location = models.CharField(
    max_length=255,
    db_index=True
)

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
class NotificationLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=255
    )

    message = models.TextField()

    status = models.CharField(
        max_length=50
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class AICall(models.Model):

    STATUS_CHOICES = (
        ('queued', 'Queued'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
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
        default='queued'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.candidate.email} - {self.status}"
class AIInterviewSession(models.Model):

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=50,
        default='started'
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )
class AIQuestion(models.Model):

    session = models.ForeignKey(
        AIInterviewSession,
        on_delete=models.CASCADE
    )

    question_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class AIAnswer(models.Model):

    question = models.ForeignKey(
        AIQuestion,
        on_delete=models.CASCADE
    )

    answer_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class CallLog(models.Model):

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    triggered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='triggered_calls'
    )

    reason = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class QuestionTemplate(models.Model):

    CATEGORY_CHOICES = (
        ('intro', 'Introduction'),
        ('experience', 'Experience'),
        ('skills', 'Skills'),
        ('availability', 'Availability'),
        ('salary', 'Salary'),
    )

    question_text = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    def __str__(self):
        return self.question_text
class JobQuestion(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        QuestionTemplate,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.job.title}"
class InterviewState(models.Model):

    session = models.ForeignKey(
        AIInterviewSession,
        on_delete=models.CASCADE
    )

    current_question_index = models.IntegerField(
        default=0
    )
class InterviewAnswer(models.Model):

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    question = models.TextField()

    answer = models.TextField()

    confidence = models.FloatField(
        default=0
    )

    ai_notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class EvaluationResult(models.Model):

    answer = models.ForeignKey(
        InterviewAnswer,
        on_delete=models.CASCADE
    )

    score = models.FloatField()

    remarks = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class InterviewSchedule(models.Model):

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    status = models.CharField(
        max_length=50,
        default="scheduled"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class AvailabilitySlot(models.Model):

    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_booked = models.BooleanField(
        default=False
    )