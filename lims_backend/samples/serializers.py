from rest_framework import serializers
from .models import (
    SampleType, RawMaterial, Packaging, FatBlend, FinishedProduct, Sample
)


class SampleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleType
        fields = "__all__"


class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = "__all__"


class PackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packaging
        fields = "__all__"


class FatBlendSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatBlend
        fields = "__all__"


class FinishedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedProduct
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    registered_by = serializers.ReadOnlyField(source="registered_by.username")

    class Meta:
        model = Sample
        fields = "__all__"
        read_only_fields = ["registered_by", "registered_at", "code", "status"]

    def create(self, validated_data):
        """
        Generate kode sample otomatis sesuai jenis.
        """
        from django.utils import timezone
        dt = timezone.now().strftime("%d%m%y")

        sample_type = validated_data.get("type")
        related_raw = validated_data.get("related_raw")
        related_finished = validated_data.get("related_finished")

        # === Kode generator ===
        if related_raw and related_raw.tank_code:
            # contoh: J3-180925
            base = related_raw.tank_code
            code = f"{base}-{dt}"
        elif related_finished and related_finished.batch_code:
            # finished pakai batch code + tanggal
            code = f"{related_finished.batch_code}-{dt}"
        else:
            # fallback default
            code = f"SMP-{dt}-{Sample.objects.count()+1}"

        validated_data["code"] = code
        validated_data["registered_by"] = self.context["request"].user
        return super().create(validated_data)
