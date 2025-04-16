# core/sync/klaviyo.py

import os
from core.models import Customer
from core.utils import fetch_with_retry

KLAVIYO_API_KEY = os.getenv('KLAVIYO_API_KEY')
KLAVIYO_BASE_URL = "https://a.klaviyo.com/api/profiles/"

def sync_klaviyo_customers():
    sync_results = {
        'customers_synced': 0
    }

    headers = {
    "Authorization": f"Bearer {KLAVIYO_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    url = f"{KLAVIYO_BASE_URL}?page[size]=100"

    response = fetch_with_retry(url, headers=headers)

    for item in response.get('data', []):
        attributes = item.get('attributes', {})
        email = attributes.get('email')
        if email:
            Customer.objects.update_or_create(
                email=email,
                defaults={
                    'first_name': attributes.get('first_name', ''),
                    'last_name': attributes.get('last_name', ''),
                    'source_platform': 'klaviyo',
                    'external_id': item.get('id')
                }
            )
            sync_results['customers_synced'] += 1

    return sync_results
