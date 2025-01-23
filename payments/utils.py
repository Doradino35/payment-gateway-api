import requests
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()  # Reads the .env file if it exists

# Fetch the Paystack secret key from the environment variables
PAYSTACK_SECRET_KEY = env("PAYSTACK_SECRET_KEY")

def initiate_payment(email, amount):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": email,
        "amount": int(amount * 100),  # Paystack expects amount in kobo
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def verify_payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
    }
    response = requests.get(url, headers=headers)
    return response.json()

