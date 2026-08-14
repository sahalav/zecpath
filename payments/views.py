from django.shortcuts import render

import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from razorpay.errors import SignatureVerificationError


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


class CreateOrderAPIView(APIView):

    def post(self, request):

        amount = request.data.get("amount", 500)

        order = client.order.create({
            "amount": amount * 100,
            "currency": "INR",
            "payment_capture": 1
        })

        return Response(order)


class VerifyPaymentAPIView(APIView):

    def post(self, request):

        try:

            params = {

                "razorpay_order_id":
                request.data.get("order_id"),

                "razorpay_payment_id":
                request.data.get("payment_id"),

                "razorpay_signature":
                request.data.get("signature")

            }

            client.utility.verify_payment_signature(
                params
            )

            return Response({
                "message": "Payment Verified"
            })

        except SignatureVerificationError:

            return Response({
                "error": "Invalid Payment"
            }, status=400)


class RazorpayWebhookAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        event = request.data.get("event")

        if event == "payment.captured":

            return Response({
                "message": "Payment Success Webhook Received"
            })

        elif event == "payment.failed":

            return Response({
                "message": "Payment Failed Webhook Received"
            })

        elif event == "refund.processed":

            return Response({
                "message": "Refund Webhook Received"
            })

        return Response({
            "message": "Unknown Event"
        })
