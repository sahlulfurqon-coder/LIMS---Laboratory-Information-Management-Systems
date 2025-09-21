from rest_framework import serializers
from .models import InventoryItem, InventoryUsage, InventoryOrder

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class InventoryUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryUsage
        fields = '__all__'

class InventoryOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryOrder
        fields = '__all__'