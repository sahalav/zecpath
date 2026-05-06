from django.urls import path
from .views import JobListAPI, JobCreateAPI, TestAPI, JobUpdateAPI, JobDeleteAPI

urlpatterns = [
    path('', JobListAPI.as_view()),
    path('create/', JobCreateAPI.as_view()),
    path('test/', TestAPI.as_view()),
    path('update/<int:id>/', JobUpdateAPI.as_view()),
    path('delete/<int:id>/', JobDeleteAPI.as_view()),
]