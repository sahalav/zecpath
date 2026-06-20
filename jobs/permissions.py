from rest_framework.permissions import BasePermission
from .models import Subscription

class PremiumAccessPermission(BasePermission):

    def has_permission(self, request, view):

        return Subscription.objects.filter(
            user=request.user,
            is_active=True
        ).exists()