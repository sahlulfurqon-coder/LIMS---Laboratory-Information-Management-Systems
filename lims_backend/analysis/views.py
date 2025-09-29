# analysis/views.py
from rest_framework import viewsets, permissions
from .models import AnalysisParameter, AnalysisResult
from .serializers import AnalysisParameterSerializer, AnalysisResultSerializer

class AnalysisParameterViewSet(viewsets.ModelViewSet):
    queryset = AnalysisParameter.objects.all()
    serializer_class = AnalysisParameterSerializer
    permission_classes = [permissions.IsAuthenticated]

class AnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = AnalysisResult.objects.all().order_by("-created_at")
    serializer_class = AnalysisResultSerializer
    permission_classes = [permissions.IsAuthenticated]

