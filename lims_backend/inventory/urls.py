from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, InventoryUsageViewSet, InventoryOrderViewSet

router = DefaultRouter()
router.register('items', InventoryItemViewSet, basename='inventory-items')
router.register('usage', InventoryUsageViewSet, basename='inventory-usage')
router.register('order', InventoryOrderViewSet, basename='inventory-order')

urlpatterns = [
    path('', include(router.urls)),
]
