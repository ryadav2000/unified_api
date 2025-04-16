from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CustomerViewSet, OrderViewSet, SyncDataView, TestKlaviyoSyncView, TestShopifySyncView, SyncKlaviyoView, SyncShopifyView

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('customers', CustomerViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [
    # ViewSets
    path('', include(router.urls)),

    # Combined Sync
    path('sync/', SyncDataView.as_view(), name='sync-data'),

    # Background Sync (Celery Tasks)
    path('api/sync/shopify/', SyncShopifyView.as_view(), name='sync-shopify'),
    path('api/sync/klaviyo/', SyncKlaviyoView.as_view(), name='sync-klaviyo'),

    # Testing Individual Syncs
    path('test-sync/shopify/', TestShopifySyncView.as_view(), name='test-sync-shopify'),
    path('test-sync/klaviyo/', TestKlaviyoSyncView.as_view(), name='test-sync-klaviyo'),
]
