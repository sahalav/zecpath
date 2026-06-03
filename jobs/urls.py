from django.urls import path

from .views import (
    JobListAPI,
    JobCreateAPI,
    TestAPI,
    JobUpdateAPI,
    JobDeleteAPI,
    ApplyJobAPI,
    UpdateApplicationStatusAPI,
    EmployerJobsAPI,
    ApplicantsAPI,
    AppliedJobsAPI,
    SaveJobAPI,
    RecommendationAPI,
    AuditLogAPI,
    ApproveEmployerAPI,
    BlockUserAPI,
    PlatformStatsAPI,
    PlatformStatsAPI,
UserGrowthAPI,
JobActivityAPI,
ATSMatchAPI,RankedCandidatesAPI,EligibilityAPI,NotificationLogsAPI,
EligibilityCheckAPIView,TriggerAICallAPIView,CallStatusAPIView
)

urlpatterns = [

    path('', JobListAPI.as_view()),

    path('create/', JobCreateAPI.as_view()),

    path('test/', TestAPI.as_view()),

    path('update/<int:id>/', JobUpdateAPI.as_view()),

    path('delete/<int:id>/', JobDeleteAPI.as_view()),

    path('apply/<int:job_id>/', ApplyJobAPI.as_view()),

    path(
        'application-status/<int:application_id>/',
        UpdateApplicationStatusAPI.as_view()
    ),

    path('my-jobs/', EmployerJobsAPI.as_view()),

    path('applicants/', ApplicantsAPI.as_view()),

    path('applied-jobs/', AppliedJobsAPI.as_view()),

    path('save-job/<int:job_id>/', SaveJobAPI.as_view()),

    path(
        'recommendations/',
        RecommendationAPI.as_view()
    ),

    path(
        'audit-logs/',
        AuditLogAPI.as_view()
    ),

    # ✅ ADMIN APIs

    path(
        'approve-employer/<int:user_id>/',
        ApproveEmployerAPI.as_view()
    ),

    path(
        'block-user/<int:user_id>/',
        BlockUserAPI.as_view()
    ),

    path(
        'platform-stats/',
        PlatformStatsAPI.as_view()
    ),
    path(
    'platform-stats/',
    PlatformStatsAPI.as_view()
),

path(
    'user-growth/',
    UserGrowthAPI.as_view()
),

path(
    'job-activity/',
    JobActivityAPI.as_view()
),
path(
    'ats-match/<int:job_id>/',
    ATSMatchAPI.as_view()
),
path(
    'ranked-candidates/',
    RankedCandidatesAPI.as_view()
),
path(
    'eligibility/<int:job_id>/',
    EligibilityAPI.as_view()
),
path(
    'notification-logs/',
    NotificationLogsAPI.as_view()
),
path(
    'check-eligibility/<int:candidate_id>/',
    EligibilityCheckAPIView.as_view()
),
path(
    'trigger-ai-call/<int:candidate_id>/',
    TriggerAICallAPIView.as_view()
),

path(
    'call-status/',
    CallStatusAPIView.as_view()
),
]