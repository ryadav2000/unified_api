from celery import shared_task
from core.sync.shopify import sync_shopify_products_and_customers
from core.sync.klaviyo import sync_klaviyo_customers

@shared_task
def sync_shopify_task():
    return sync_shopify_products_and_customers()

@shared_task
def sync_klaviyo_task():
    return sync_klaviyo_customers()