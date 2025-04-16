import os
from core.models import Product, Customer
from core.utils import fetch_with_retry

SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_PASSWORD = os.getenv('SHOPIFY_PASSWORD')
SHOPIFY_STORE_NAME = os.getenv('SHOPIFY_STORE_NAME')

BASE_URL = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOPIFY_STORE_NAME}.myshopify.com/admin/api/2023-10"

def sync_shopify_products_and_customers():
    sync_results = {
        'products_synced': 0,
        'customers_synced': 0,
    }

    # --- Sync Products ---
    product_url = f"{BASE_URL}/products.json?limit=250"
    products_data = fetch_with_retry(product_url)

    for product in products_data.get('products', []):
        # We'll just take the first variant (you can expand if needed)
        variant = product['variants'][0]
        Product.objects.update_or_create(
            sku=variant['sku'],
            defaults={
                'name': product['title'],
                'price': variant['price'],
                'inventory_count': variant['inventory_quantity'],
                'source_platform': 'shopify',
                'external_id': product['id'],
            }
        )
        sync_results['products_synced'] += 1

    # --- Sync Customers ---
    customer_url = f"{BASE_URL}/customers.json?limit=250"
    customers_data = fetch_with_retry(customer_url)

    for customer in customers_data.get('customers', []):
        Customer.objects.update_or_create(
            email=customer['email'],
            defaults={
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'source_platform': 'shopify',
                'external_id': customer['id'],
            }
        )
        sync_results['customers_synced'] += 1

    return sync_results
