# samples/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from .models import (
    SampleType, RawMaterial, Packaging, FatBlend, FinishedProduct, Sample
)
from .serializers import (
    SampleTypeSerializer, RawMaterialSerializer, PackagingSerializer,
    FatBlendSerializer, FinishedProductSerializer, SampleSerializer
)


class SampleTypeViewSet(viewsets.ModelViewSet):
    queryset = SampleType.objects.all()
    serializer_class = SampleTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class RawMaterialViewSet(viewsets.ModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]


class PackagingViewSet(viewsets.ModelViewSet):
    queryset = Packaging.objects.all()
    serializer_class = PackagingSerializer
    permission_classes = [permissions.IsAuthenticated]


class FatBlendViewSet(viewsets.ModelViewSet):
    queryset = FatBlend.objects.all()
    serializer_class = FatBlendSerializer
    permission_classes = [permissions.IsAuthenticated]


class FinishedProductViewSet(viewsets.ModelViewSet):
    queryset = FinishedProduct.objects.all()
    serializer_class = FinishedProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.exclude(status="deleted").order_by("-registered_at")
    serializer_class = SampleSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["type", "urgency", "requester", "status"]
    search_fields = ["code", "requester", "notes"]

    def perform_destroy(self, instance):
        user = self.request.user
        if hasattr(user, "role") and user.role in ["admin", "qa_manager"]:
            instance.status = "deleted"
            instance.save()
        else:
            raise PermissionDenied("Hanya Admin/QA Manager yang bisa menghapus sampel.")
