from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .utils import initiate_payment, verify_payment

class PaymentInitiateView(APIView):
    def post(self, request):
        data = request.data
        customer_name = data.get("customer_name")
        customer_email = data.get("customer_email")
        amount = data.get("amount")
        if not customer_name or not customer_email or not amount:
            return Response({"status": "error", "message": "Missing fields."}, status=status.HTTP_400_BAD_REQUEST)

        response = initiate_payment(customer_email, amount)
        if response.get("status"):
            payment = Payment.objects.create(
                id=response["data"]["reference"],
                customer_name=customer_name,
                customer_email=customer_email,
                amount=amount,
            )
            return Response({"status": "success", "data": response["data"]}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": "Payment initiation failed."}, status=status.HTTP_400_BAD_REQUEST)

class PaymentStatusView(APIView):
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id)
            response = verify_payment(payment_id)
            if response.get("status"):
                payment.status = response["data"]["status"]
                payment.save()
                return Response({
                    "payment": {
                        "id": payment.id,
                        "customer_name": payment.customer_name,
                        "customer_email": payment.customer_email,
                        "amount": payment.amount,
                        "status": payment.status,
                    },
                    "status": "success",
                    "message": "Payment details retrieved successfully."
                })
            return Response({"status": "error", "message": "Payment verification failed."}, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response({"status": "error", "message": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

