from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Specification
from .serializers import SpecificationSerializer
from django.utils import timezone

class SpecificationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') not in ['rnd','qa_manager']:
            return Response({"detail": "Hanya RnD/QA Manager yang bisa membuat spesifikasi"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') not in ['rnd','qa_manager']:
            return Response({"detail": "Hanya RnD/QA Manager yang bisa merevisi spesifikasi"}, status=status.HTTP_403_FORBIDDEN)
        # versioning otomatis
        instance = self.get_object()
        instance.version += 1
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_spec(self, request, pk=None):
        user = request.user
        if getattr(user, 'role', '') != 'qa_manager':
            return Response({"detail": "Hanya QA Manager yang bisa approve spesifikasi"}, status=status.HTTP_403_FORBIDDEN)
        
        spec = get_object_or_404(Specification, pk=pk)
        spec.status = 'approved'
        spec.approved_by = user
        spec.approved_at = timezone.now()
        spec.save()
        serializer = self.get_serializer(spec)
        return Response(serializer.data)
