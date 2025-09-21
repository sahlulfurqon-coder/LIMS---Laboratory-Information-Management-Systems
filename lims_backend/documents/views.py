from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.filter(status='active').order_by('-created_at')
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') not in ['qa_supervisor', 'qa_manager']:
            return Response({"detail": "Hanya QA Supervisor/Manager yang bisa upload dokumen"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') not in ['qa_supervisor', 'qa_manager']:
            return Response({"detail": "Hanya QA Supervisor/Manager yang bisa revisi dokumen"}, status=status.HTTP_403_FORBIDDEN)
        
        # Auto versioning
        instance = self.get_object()
        instance.version += 1
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') != 'qa_manager':
            return Response({"detail": "Hanya QA Manager yang bisa arsipkan dokumen"}, status=status.HTTP_403_FORBIDDEN)
        
        instance = self.get_object()
        instance.status = 'archived'
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

