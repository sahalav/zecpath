from django.urls import path
from .views import JobListAPI, JobCreateAPI, TestAPI,JobUpdateAPI,JobDeleteAPI

urlpatterns = [
    path('jobs/', JobListAPI.as_view()),
    path('jobs/create/', JobCreateAPI.as_view()),
    path('test/', TestAPI.as_view()),
    path('jobs/update/<int:id>/', JobUpdateAPI.as_view()),
    path('jobs/delete/<int:id>/', JobDeleteAPI.as_view()),
]