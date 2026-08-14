from django.urls import path
from .views import CreateOrderAPIView, VerifyPaymentAPIView, RazorpayWebhookAPIView

urlpatterns = [
    path(
        "create-order/",
        CreateOrderAPIView.as_view()
    ),
    path(
        "verify/",
        VerifyPaymentAPIView.as_view()
    ),
    path(
        "webhook/",
        RazorpayWebhookAPIView.as_view()
    ),
]
