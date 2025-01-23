from unittest.mock import patch
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from payments.models import Payment
from rest_framework import status

class PaymentAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.payment_status_url = lambda payment_id: reverse('payment-status', args=[payment_id])

    @patch("payments.utils.verify_payment")  # Correct placement of the @patch decorator
    def test_payment_status_completed(self, mock_verify_payment):
        """Test retrieving the status of a successfully verified payment."""
        # Create a payment record in the database
        payment = Payment.objects.create(
            id="PAY-54712",
            customer_name="Dora Dino",
            customer_email="doradino35@gmail.com",
            amount=200.00,
            status="pending",
        )
    
        # Mock the verification response
        mock_verify_payment.return_value = {
            "status": True,
            "data": {"status": "completed"},
        }
    
        # Send GET request to retrieve payment status
        response = self.client.get(self.payment_status_url(payment.id))
    
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["payment"]["id"], payment.id)
        self.assertEqual(response.json()["payment"]["status"], "completed")
