from rest_framework import serializers
from .models import ExternalRequest, ProductDevRequest
from .models import ExternalAnalysisResult

class ExternalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalRequest
        fields = "__all__"

class ProductDevRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDevRequest
        fields = "__all__"

class ExternalAnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalAnalysisResult
        fields = '__all__'