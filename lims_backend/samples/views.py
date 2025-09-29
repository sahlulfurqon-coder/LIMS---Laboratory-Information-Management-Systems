from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Sample, RawMaterial, SampleType, FatBlend, Packaging, FinishedProduct
from .serializers import (
    SampleSerializer,
    RawMaterialSerializer,
    SampleTypeSerializer,
    FatBlendSerializer,
    PackagingSerializer,
    FinishedProductSerializer,
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
    filterset_fields = ["type", "urgency", "status"]   # requester dihapus
    search_fields = ["code", "notes"]                  # requester dihapus

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        sample = self.get_object()
        if not request.user.groups.filter(name__in=["QA Manager", "QA Supervisor", "Admin"]).exists():
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        sample.status = "completed"   # ✅ samain dengan models
        sample.approved_by = request.user
        sample.approval_note = request.data.get("note", "")
        sample.save()
        return Response({"status": "completed"})

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        sample = self.get_object()
        if not request.user.groups.filter(name__in=["QA Manager", "QA Supervisor", "Admin"]).exists():
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        sample.status = "processing"   # bisa juga bikin "rejected" kalau mau tambahin di choices
        sample.approved_by = request.user
        sample.approval_note = request.data.get("note", "")
        sample.save()
        return Response({"status": "processing"})

    def perform_destroy(self, instance):
        user = self.request.user
        if hasattr(user, "role") and user.role in ["admin", "qa_manager"]:
            instance.status = "deleted"
            instance.save()
        else:
            raise PermissionDenied("Hanya Admin/QA Manager yang bisa menghapus sampel.")
