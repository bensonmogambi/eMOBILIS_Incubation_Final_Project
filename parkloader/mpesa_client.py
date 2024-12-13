import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

class MpesaClient:
    def __init__(self):
        # Fetching the Mpesa credentials from settings.py
        self.environment = settings.MPESA_ENVIRONMENT
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.express_shortcode = settings.MPESA_EXPRESS_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.username = settings.MPESA_INITIATOR_USERNAME
        self.security_credentials = settings.MPESA_INITIATOR_SECURITY_CREDENTIALS
        self.lipa_na_mpesa_url = f"https://{self.environment}.safaricom.co.ke/mpesa/express/v1/checkout"
        self.oauth_url = f"https://{self.environment}.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    def get_access_token(self):
        """ Get the access token for Mpesa API """
        response = requests.get(self.oauth_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        if response.status_code == 200:
            json_response = response.json()
            return json_response['access_token']
        else:
            raise Exception("Unable to fetch access token from Mpesa")

    def stk_push(self, phone_number, amount, account_reference, transaction_desc, callback_url):
        """ Initiate STK Push to prompt payment """
        access_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            "Shortcode": self.shortcode,
            "Amount": amount,
            "PhoneNumber": phone_number,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc,
            "CallbackURL": callback_url
        }

        response = requests.post(self.lipa_na_mpesa_url, json=payload, headers=headers)
        return response.json()
