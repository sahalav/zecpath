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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
