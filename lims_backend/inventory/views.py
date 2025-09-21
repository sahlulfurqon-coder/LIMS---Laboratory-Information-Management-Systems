from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from .models import InventoryItem, InventoryUsage, InventoryOrder
from .serializers import InventoryItemSerializer, InventoryUsageSerializer, InventoryOrderSerializer

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        # alert stok <20% dari min_stock
        items = InventoryItem.objects.filter(quantity__lt=models.F('min_stock')*0.2)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

class InventoryUsageViewSet(viewsets.ModelViewSet):
    queryset = InventoryUsage.objects.all()
    serializer_class = InventoryUsageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        usage = serializer.save(used_by=self.request.user)
        # update stok item
        usage.item.quantity -= usage.quantity
        usage.item.save()

class InventoryOrderViewSet(viewsets.ModelViewSet):
    queryset = InventoryOrder.objects.all()
    serializer_class = InventoryOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

