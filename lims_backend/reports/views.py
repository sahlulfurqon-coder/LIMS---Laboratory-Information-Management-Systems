from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditTrail
from .serializers import (
    SampleReportSerializer, 
    ComplaintReportSerializer,
    SpecsReportSerializer,
    AuditTrailSerializer, ExternalAnalysisReportSerializer
)
from requests.models import ExternalAnalysisResult
from samples.models import Sample
from complaints.models import Complaint
from specs.models import Specification

class ReportsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def samples(self, request):
        queryset = Sample.objects.all()
        # optional filtering
        status = request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        serializer = SampleReportSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def complaints(self, request):
        queryset = Complaint.objects.all()
        status = request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        serializer = ComplaintReportSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def specs(self, request):
        queryset = Specification.objects.all()
        serializer = SpecsReportSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def audit(self, request):
        queryset = AuditTrail.objects.all().order_by('-timestamp')
        serializer = AuditTrailSerializer(queryset, many=True)
        return Response(serializer.data)

class ExternalAnalysisReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExternalAnalysisResult.objects.all()
    serializer_class = ExternalAnalysisReportSerializer
