from django.urls import path
from .views import PaymentInitiateView, PaymentStatusView

urlpatterns = [
    path('api/v1/payments', PaymentInitiateView.as_view(), name='initiate-payment'),
    path('api/v1/payments/<str:payment_id>/', PaymentStatusView.as_view(), name='payment-status'),
]

