from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Complaint, CAPA
from .serializers import ComplaintSerializer, CAPASerializer

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all().order_by('-created_at')
    serializer_class = ComplaintSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') not in ['qa_supervisor', 'qa_manager']:
            return Response({"detail": "Hanya QA Supervisor/Manager yang bisa update status"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='capa')
    def add_capa(self, request, pk=None):
        user = request.user
        if getattr(user, 'role', '') != 'qa_manager':
            return Response({"detail": "Hanya QA Manager yang bisa menambahkan CAPA"}, status=status.HTTP_403_FORBIDDEN)
        
        complaint = get_object_or_404(Complaint, pk=pk)
        serializer = CAPASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(complaint=complaint)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CAPA(viewsets.ModelViewSet):
    queryset = CAPA.objects.all().order_by('-created_at')
    serializer_class = CAPASerializer
