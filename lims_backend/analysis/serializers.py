# analysis/serializers.py
from rest_framework import serializers
from .models import AnalysisResult, AnalysisParameter
from samples.serializers import SampleSerializer

from rest_framework import serializers
from .models import AnalysisParameter, AnalysisResult

class AnalysisParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisParameter
        fields = "__all__"

class AnalysisResultSerializer(serializers.ModelSerializer):
    parameter_name = serializers.CharField(source="parameter.name", read_only=True)

    class Meta:
        model = AnalysisResult
        fields = [
            "id", "sample", "parameter", "parameter_name",
            "value", "status", "analyst", "note", "created_at"
        ]
        read_only_fields = ["analyst", "status", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["analyst"] = request.user
        return super().create(validated_data)

