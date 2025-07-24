# api/mpesa_api.py

import requests
import base64
from datetime import datetime
from django.conf import settings
from django.core.cache import cache 

def get_mpesa_access_token():
    """
    Fetches M-Pesa access token and caches it.
    """
    cached_token = cache.get('mpesa_access_token')
    if cached_token:
        return cached_token

    if settings.MPESA_ENVIRONMENT == 'production':
        url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    else:
        url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    try:
        response = requests.get(url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET), timeout=10)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Error getting access token: {e}")
        return None

    try:
        token = response.json()['access_token']
        cache.set('mpesa_access_token', token, timeout=3500) # Cache for just under an hour
        return token
    except KeyError:
        print("Could not find 'access_token' in the response.")
        return None
