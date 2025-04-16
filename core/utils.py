import time
import requests
from requests.exceptions import RequestException

def fetch_with_retry(url, headers=None, max_retries=3):
    backoff = 1
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 429:
                time.sleep(backoff)
                backoff *= 2
            elif response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
        except RequestException:
            time.sleep(backoff)
            backoff *= 2
    raise Exception("Max retries exceeded.")
