from rest_framework.permissions import BasePermission
from .models import Subscription


class PremiumAccessPermission(BasePermission):

    def has_permission(self, request, view):

        return Subscription.objects.filter(
            user=request.user,
            is_active=True
        ).exists()


class PremiumRecruiterPermission(BasePermission):

    def has_permission(self, request, view):

        print("EMAIL =", request.user.email)
        print("ROLE =", request.user.role)

        subscription = Subscription.objects.filter(
            user=request.user,
            is_active=True
        ).first()

        print("SUB =", subscription)

        if request.user.role != "employer":
            return False

        return Subscription.objects.filter(
            user=request.user,
            is_active=True
        ).exists()