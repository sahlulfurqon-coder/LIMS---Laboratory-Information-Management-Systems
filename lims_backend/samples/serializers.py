from rest_framework import serializers
from django.utils import timezone
from .models import (
    SampleType, RawMaterial, Packaging, FatBlend, FatBlendComponent,
    FinishedProduct, Sample, Tank, TransferRawMaterial
)
from django.db import transaction

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


class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = "__all__"


class TransferRawMaterialSerializer(serializers.ModelSerializer):
    sample_code = serializers.CharField(read_only=True, source="sample_code")
    class Meta:
        model = TransferRawMaterial
        fields = "__all__"
        read_only_fields = ("requested_by","requested_at","approved_by","approved_at","status")

    def create(self, validated_data):
        # compute transfer_no as next integer for that to_tank on that date
        to_tank = validated_data.get("to_tank")
        transfer_date = validated_data.get("transfer_date", timezone.now().date())
        last = TransferRawMaterial.objects.filter(to_tank=to_tank, transfer_date=transfer_date).order_by("-transfer_no").first()
        next_no = 1 if not last else last.transfer_no + 1
        validated_data["transfer_no"] = next_no
        request_user = self.context["request"].user
        validated_data["requested_by"] = request_user
        tr = super().create(validated_data)
        return tr


class FatBlendComponentSerializer(serializers.ModelSerializer):
    tank = TankSerializer(read_only=True)
    tank_id = serializers.PrimaryKeyRelatedField(queryset=Tank.objects.all(), source="tank", write_only=True)
    class Meta:
        model = FatBlendComponent
        fields = ("id","tank","tank_id","percentage")


class FatBlendSerializer(serializers.ModelSerializer):
    components = FatBlendComponentSerializer(many=True)
    class Meta:
        model = FatBlend
        fields = ("id","code","created_by","created_at","notes","components")
        read_only_fields = ("created_by","created_at")

    def create(self, validated_data):
        comps = validated_data.pop("components", [])
        request_user = self.context["request"].user
        with transaction.atomic():
            fb = FatBlend.objects.create(created_by=request_user, **validated_data)
            total = 0
            for c in comps:
                FatBlendComponent.objects.create(fatblend=fb, tank=c["tank"], percentage=c["percentage"])
                total += float(c["percentage"])
            if round(total,2) != 100.00:
                raise serializers.ValidationError("Total composition percentage must equal 100.")
        return fb


class FinishedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedProduct
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = "__all__"
        read_only_fields = ("registered_by","registered_at","code")

    def create(self, validated_data):
        # generate sample code based on sample_type and raw_meta information
        dt = timezone.now().strftime("%d%m%y")
        sample_type = validated_data.get("sample_type")
        ref = validated_data.get("reference_id")
        registered_by = self.context["request"].user

        # default code
        code = f"SMP-{dt}-{Sample.objects.count()+1}"

        # if this sample references a TransferRawMaterial, try use its sample_code
        if sample_type == "raw_material" and ref:
            try:
                tr = TransferRawMaterial.objects.get(pk=ref)
                code = tr.sample_code()
            except TransferRawMaterial.DoesNotExist:
                pass

        validated_data["code"] = code
        validated_data["registered_by"] = registered_by
        return super().create(validated_data)
