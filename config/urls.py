"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView


schema_view = get_schema_view(
    openapi.Info(
        title="ZecPath API",
        default_version="v1",
        description="API Documentation for ZecPath",
        contact=openapi.Contact(
            email="support@zecpath.com"
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [

    path(
        "",
        RedirectView.as_view(
            url="/swagger/",
            permanent=False
        ),
    ),

    path(
        "swagger/",
        schema_view.with_ui(
            "swagger",
            cache_timeout=0
        ),
        name="swagger-ui",
    ),

    path(
        "redoc/",
        schema_view.with_ui(
            "redoc",
            cache_timeout=0
        ),
        name="redoc",
    ),

    path("admin/", admin.site.urls),

    path("api/", include("accounts.urls")),

    path("api/jobs/", include("jobs.urls")),

    path(
        "api/payments/",
        include("payments.urls"),
    ),

] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)