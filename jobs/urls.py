from django.urls import path

from .views import (
    JobListAPI,
    JobCreateAPI,
    TestAPI,
    JobUpdateAPI,
    JobDeleteAPI,
    ApplyJobAPI,
    UpdateApplicationStatusAPI,EmployerJobsAPI,
    ApplicantsAPI
)

urlpatterns = [

    path('', JobListAPI.as_view()),

    path('create/', JobCreateAPI.as_view()),

    path('test/', TestAPI.as_view()),

    path('update/<int:id>/', JobUpdateAPI.as_view()),

    path('delete/<int:id>/', JobDeleteAPI.as_view()),

    path('apply/<int:job_id>/', ApplyJobAPI.as_view()),

    # ATS Status Update
    path(
        'application-status/<int:application_id>/',
        UpdateApplicationStatusAPI.as_view()
    ),
    path('my-jobs/', EmployerJobsAPI.as_view()),
    path('applicants/', ApplicantsAPI.as_view()),

]