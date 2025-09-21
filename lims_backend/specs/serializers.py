from rest_framework import serializers
from .models import Specification

class SpecificationSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    approved_by_username = serializers.CharField(source='approved_by.username', read_only=True)

    class Meta:
        model = Specification
        fields = "__all__"
