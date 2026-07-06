from django.urls import path
from .views import (
    signup,
    profile,
    ProtectedView,
    AdminView,
    EmployerView,
    CandidateView,
    create_candidate_profile,
    view_candidate_profile,
    update_candidate_profile,
    delete_candidate_profile,
    upload_resume,
    download_resume,
    delete_resume,
    UserListView, ApproveEmployerAPI,
    FlaggedUsersAPI,FlagUserAPI,ResumeParserAPI
    

)

from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('protected/', ProtectedView.as_view(), name='protected'),

    path('admin-panel/', AdminView.as_view(), name='admin-panel'),
    path('employer-panel/', EmployerView.as_view(), name='employer-panel'),
    path('candidate-panel/', CandidateView.as_view(), name='candidate-panel'),
    path('candidate-profile/create/', create_candidate_profile),
path('candidate-profile/view/', view_candidate_profile),
path('candidate-profile/update/', update_candidate_profile),
path('candidate-profile/delete/', delete_candidate_profile),
path('resume/upload/', upload_resume),
path('resume/download/', download_resume),
path(
    "resume/delete/",
    delete_resume
),
path('users/', UserListView.as_view()),
path(
    'approve-employer/<int:user_id>/',
    ApproveEmployerAPI.as_view()
),
path(
    'flagged-users/',
    FlaggedUsersAPI.as_view()
),
path(
    'flag-user/<int:user_id>/',
    FlagUserAPI.as_view()
),
path(
    'resume-parse/',
    ResumeParserAPI.as_view()
),
]
