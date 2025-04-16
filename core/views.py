from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product, Customer, Order
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer
from .sync.shopify import sync_shopify_products_and_customers
from .sync.klaviyo import sync_klaviyo_customers
from .tasks import sync_shopify_task, sync_klaviyo_task

import logging
logger = logging.getLogger(__name__)


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sku', 'source_platform', 'price']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'source_platform']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'source_platform']



class SyncDataView(APIView):
    def post(self, request):
        results = {}
        try:
            shopify_result = sync_shopify_products_and_customers()
            results['shopify'] = shopify_result
        except Exception as e:
            logger.error(f"Shopify sync failed: {str(e)}")
            results['shopify'] = f"Failed: {str(e)}"

        try:
            klaviyo_result = sync_klaviyo_customers()
            results['klaviyo'] = klaviyo_result
        except Exception as e:
            logger.error(f"Klaviyo sync failed: {str(e)}")
            results['klaviyo'] = f"Failed: {str(e)}"

        return Response(results, status=status.HTTP_200_OK)
    

class TestShopifySyncView(APIView):
    @swagger_auto_schema(
        operation_summary="Test sync from Shopify",
        operation_description="This endpoint fetches sample data from the Shopify API using the API key and store credentials defined in the environment.",
        responses={
            200: openapi.Response(description="Successfully fetched Shopify data."),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def post(self, request):
        result = sync_shopify_products_and_customers()  # or your actual sync logic
        return Response({"message": "Shopify sync complete", "result": result})

class TestKlaviyoSyncView(APIView):
    @swagger_auto_schema(
        operation_summary="Test sync from Klaviyo",
        operation_description="This endpoint fetches sample customer data from the Klaviyo API using the API key provided in the .env file.",
        responses={
            200: openapi.Response(description="Successfully fetched Klaviyo data."),
            400: "Bad Request",
            401: "Unauthorized",
            500: "Internal Server Error"
        }
    )
    def post(self, request):
        result = sync_klaviyo_customers()
        return Response({"message": "Klaviyo sync complete", "result": result})
    

class SyncShopifyView(APIView):
    def post(self, request):
        sync_shopify_task.delay()  # Run in background
        return Response({"message": "Shopify sync started."}, status=status.HTTP_202_ACCEPTED)

class SyncKlaviyoView(APIView):
    def post(self, request):
        sync_klaviyo_task.delay()
        return Response({"message": "Klaviyo sync started."}, status=status.HTTP_202_ACCEPTED)