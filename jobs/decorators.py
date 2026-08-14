from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from jobs.models import Subscription
from datetime import date


def subscription_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        subscription = Subscription.objects.filter(
            user=request.user,
            is_active=True,
            end_date__gte=date.today()
        ).first()

        if not subscription:
            return Response(
                {"error": "Active subscription required"},
                status=status.HTTP_403_FORBIDDEN
            )

        return view_func(request, *args, **kwargs)

    return wrapper
