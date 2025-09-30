from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Sample, RawMaterial, SampleType, FatBlend, Packaging, FinishedProduct,
    Tank, TransferRawMaterial
)
from .serializers import (
    SampleSerializer, RawMaterialSerializer, SampleTypeSerializer,
    FatBlendSerializer, PackagingSerializer, FinishedProductSerializer,
    TankSerializer, TransferRawMaterialSerializer
)

# ===== Read-only untuk dropdown =====
class SampleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SampleType.objects.all()
    serializer_class = SampleTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class RawMaterialViewSet(viewsets.ModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # prevent deletion of non-editable master data
        if not instance.editable and not self.request.user.is_superuser:
            raise PermissionDenied("Raw material master cannot be deleted.")
        instance.delete()

    def perform_update(self, serializer):
        if not serializer.instance.editable and not self.request.user.is_superuser:
            raise PermissionDenied("Raw material master cannot be updated.")
        serializer.save()


class PackagingViewSet(viewsets.ModelViewSet):
    queryset = Packaging.objects.all()
    serializer_class = PackagingSerializer
    permission_classes = [permissions.IsAuthenticated]


class TankViewSet(viewsets.ModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransferRawMaterialViewSet(viewsets.ModelViewSet):
    queryset = TransferRawMaterial.objects.all().order_by("-transfer_date","-transfer_no")
    serializer_class = TransferRawMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        transfer = self.get_object()
        user = request.user
        if not user.is_superuser and user.role not in ["QA Manager","QA Supervisor","Admin"]:
            return Response({"detail":"Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        # mark as approved and update target tank
        transfer.status = "APPROVED"
        transfer.approved_by = user
        transfer.approved_at = timezone.now()
        transfer.save()
        # update tank current_transfer pointer
        try:
            tank = Tank.objects.get(code=transfer.to_tank)
            tank.current_transfer = transfer
            tank.save()
        except Tank.DoesNotExist:
            pass
        return Response({"status":"approved"})


class FatBlendViewSet(viewsets.ModelViewSet):
    queryset = FatBlend.objects.all()
    serializer_class = FatBlendSerializer
    permission_classes = [permissions.IsAuthenticated]


class FinishedProductViewSet(viewsets.ModelViewSet):
    queryset = FinishedProduct.objects.all()
    serializer_class = FinishedProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.exclude(status="DELETED").order_by("-registered_at")
    serializer_class = SampleSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["sample_type", "urgency", "status"]
    search_fields = ["code", "notes"]

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        sample = self.get_object()
        user = request.user
        if not user.is_superuser and user.role not in ["QA Manager","QA Supervisor","Admin"]:
            return Response({"detail":"Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        sample.status = "APPROVED"
        sample.approved_by = user
        sample.approval_note = request.data.get("note","")
        sample.approved_at = timezone.now()
        sample.save()
        return Response({"status":"approved"})

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        sample = self.get_object()
        user = request.user
        if not user.is_superuser and user.role not in ["QA Manager","QA Supervisor","Admin"]:
            return Response({"detail":"Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        sample.status = "REJECTED"
        sample.approved_by = user
        sample.approval_note = request.data.get("note","")
        sample.save()
        return Response({"status":"rejected"})

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_superuser or (hasattr(user,"role") and user.role in ["Admin","QA Manager"]):
            instance.status = "DELETED"
            instance.save()
        else:
            raise PermissionDenied("Hanya Admin/QA Manager yang bisa menghapus sampel.")
