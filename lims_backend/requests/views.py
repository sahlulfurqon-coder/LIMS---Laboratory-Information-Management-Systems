from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ExternalRequest, ProductDevRequest, ExternalAnalysisResult
from .serializers import ExternalRequestSerializer, ProductDevRequestSerializer, ExternalAnalysisResultSerializer

class ExternalRequestViewSet(viewsets.ModelViewSet):
    queryset = ExternalRequest.objects.all().order_by('-created_at')
    serializer_class = ExternalRequestSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') != 'qa_manager':
            return Response({"detail": "Hanya QA Manager yang bisa membuat permintaan eksternal"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') != 'qa_supervisor':
            return Response({"detail": "Hanya QA Supervisor yang bisa update status request"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class ProductDevRequestViewSet(viewsets.ModelViewSet):
    queryset = ProductDevRequest.objects.all().order_by('-created_at')
    serializer_class = ProductDevRequestSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') != 'rnd':
            return Response({"detail": "Hanya RnD yang bisa membuat request product development"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if getattr(user, 'role', '') != 'rnd':
            return Response({"detail": "Hanya RnD yang bisa update trial results"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
class ExternalAnalysisResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExternalAnalysisResult.objects.all()
    serializer_class = ExternalAnalysisResultSerializer


