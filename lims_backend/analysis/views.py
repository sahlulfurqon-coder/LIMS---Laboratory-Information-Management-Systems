# analysis/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import AnalysisResult, AnalysisParameter
from .serializers import AnalysisResultSerializer, AnalysisParameterSerializer
from samples.models import Sample

class AnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer
    permission_classes = [IsAuthenticated]

    # POST /api/analysis/assign
    @action(detail=False, methods=['post'], url_path='assign')
    def assign_sample(self, request):
        user = request.user
        if not getattr(user, 'role', '') in ['qa_supervisor']:
            return Response({"detail": "Hanya QA Supervisor yang bisa assign sampel"}, status=status.HTTP_403_FORBIDDEN)
        
        sample_id = request.data.get('sample_id')
        analyst_id = request.data.get('analyst_id')
        parameters = request.data.get('parameters', [])
        
        sample = get_object_or_404(Sample, id=sample_id)
        for param_id in parameters:
            AnalysisResult.objects.get_or_create(
                sample=sample,
                parameter_id=param_id,
                defaults={'analyst_id': analyst_id, 'status':'in_progress'}
            )
        return Response({"detail": "Sampel berhasil diassign"}, status=status.HTTP_200_OK)

    # POST /api/analysis/{sample_id}/result
    @action(detail=True, methods=['post'], url_path='result')
    def submit_result(self, request, pk=None):
        sample = get_object_or_404(Sample, pk=pk)
        data = request.data
        user = request.user
        
        result = get_object_or_404(AnalysisResult, sample=sample, parameter_id=data['parameter'])
        if result.analyst != user:
            return Response({"detail": "Hanya analyst yang ditugaskan yang bisa submit hasil"}, status=status.HTTP_403_FORBIDDEN)
        
        result.value = data.get('value')
        result.notes = data.get('notes','')
        result.status = 'completed'
        result.save()
        serializer = self.get_serializer(result)
        return Response(serializer.data)

    # POST /api/analysis/{id}/validate
    @action(detail=True, methods=['post'], url_path='validate')
    def validate_result(self, request, pk=None):
        user = request.user
        if not getattr(user, 'role', '') in ['qa_supervisor', 'qa_manager']:
            return Response({"detail": "Hanya QA Supervisor/Manager yang bisa validasi"}, status=status.HTTP_403_FORBIDDEN)
        
        result = get_object_or_404(AnalysisResult, pk=pk)
        action_type = request.data.get('action')
        if action_type == 'approve':
            result.status = 'validated'
        else:
            result.status = 'rejected'
        result.validated_by = user
        result.validated_at = timezone.now()
        result.save()
        serializer = self.get_serializer(result)
        return Response(serializer.data)

    # POST /api/analysis/{id}/release
    @action(detail=True, methods=['post'], url_path='release')
    def release_result(self, request, pk=None):
        user = request.user
        if getattr(user, 'role', '') != 'qa_manager':
            return Response({"detail": "Hanya QA Manager yang bisa release hasil"}, status=status.HTTP_403_FORBIDDEN)
        
        result = get_object_or_404(AnalysisResult, pk=pk)
        result.status = 'released'
        result.save()
        # generate report logic bisa ditempel di sini
        return Response({"detail": f"Hasil {result.parameter.name} sample {result.sample.code} telah direlease"}, status=status.HTTP_200_OK)

class AnalysisParameterViewSet(viewsets.ModelViewSet):
    queryset = AnalysisParameter.objects.all()
    serializer_class = AnalysisParameterSerializer
    permission_classes = [IsAuthenticated]
