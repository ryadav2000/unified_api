from django.db import models

# Create your models here.
PLATFORM_CHOICES = [
    ('shopify', 'Shopify'),
    ('klaviyo', 'Klaviyo'),
    ('tock', 'Tock'),
    # Add others as needed
]

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.IntegerField()
    source_platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    external_id = models.CharField(max_length=100)  # External platform ID

    def __str__(self):
        return self.name

class Customer(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    source_platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    external_id = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    source_platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)

    def __str__(self):
        return self.order_id