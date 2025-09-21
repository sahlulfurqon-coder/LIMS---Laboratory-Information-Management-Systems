# analysis/serializers.py
from rest_framework import serializers
from .models import AnalysisResult, AnalysisParameter
from samples.serializers import SampleSerializer

class AnalysisParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisParameter
        fields = "__all__"


class AnalysisResultSerializer(serializers.ModelSerializer):
    sample_detail = SampleSerializer(source="sample", read_only=True)
    parameter_name = serializers.CharField(source="parameter.name", read_only=True)
    analyst_username = serializers.CharField(source="analyst.username", read_only=True)
    validated_by_username = serializers.CharField(source="validated_by.username", read_only=True)

    class Meta:
        model = AnalysisResult
        fields = "__all__"
