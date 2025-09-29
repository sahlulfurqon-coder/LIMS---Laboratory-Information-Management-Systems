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
    subtype = serializers.ReadOnlyField()  # ambil dari method subtype() di models

    class Meta:
        model = Sample
        fields = "__all__"
        read_only_fields = ["registered_by", "registered_at", "code", "status"]

    def create(self, validated_data):
        """
        Generate kode sample otomatis sesuai jenis.
        Format:
          - Raw material + tank → J2-210925
          - Finished product    → batchcode-210925
          - Default             → SMP-210925-<count>
        """
        from django.utils import timezone
        dt = timezone.now().strftime("%d%m%y")

        sample_type = validated_data.get("type")
        raw_detail = validated_data.get("detail")
        tank = validated_data.get("tank")

        # === Kode generator ===
        if raw_detail and tank:
            # contoh: J3-210925
            base = tank
            code = f"{base}-{dt}"
        else:
            # fallback default
            code = f"SMP-{dt}-{Sample.objects.count()+1}"

        validated_data["code"] = code
        validated_data["registered_by"] = self.context["request"].user
        return super().create(validated_data)
