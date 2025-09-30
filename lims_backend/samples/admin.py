from django.contrib import admin
from .models import (
    Sample, SampleType, RawMaterial, Packaging,
    Tank, TransferRawMaterial,
    FatBlend, FatBlendComponent,
    FinishedProduct
)


@admin.register(SampleType)
class SampleTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "description")
    search_fields = ("code", "name")


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "editable")
    list_filter = ("editable",)
    search_fields = ("name",)


@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subtype", "editable")
    list_filter = ("editable", "subtype")
    search_fields = ("name", "subtype")


@admin.register(Tank)
class TankAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "capacity", "current_transfer")
    search_fields = ("code",)


@admin.register(TransferRawMaterial)
class TransferRawMaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "from_tank", "to_tank", "raw_material", "transfer_date", "transfer_no", "status")
    list_filter = ("status", "transfer_date", "to_tank")
    search_fields = ("raw_material__name", "to_tank")


@admin.register(FatBlend)
class FatBlendAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "created_by", "created_at", "notes")
    search_fields = ("code",)


@admin.register(FatBlendComponent)
class FatBlendComponentAdmin(admin.ModelAdmin):
    list_display = ("id", "fatblend", "tank", "percentage")
    list_filter = ("tank",)
    search_fields = ("fatblend__code", "tank__code")


@admin.register(FinishedProduct)
class FinishedProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "batch_code", "production_code", "line", "fatblend", "packaging", "created_at")
    list_filter = ("line", "packaging", "created_at")
    search_fields = ("name", "batch_code", "production_code")


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "sample_type", "registered_by", "registered_at", "status", "urgency")
    list_filter = ("sample_type", "status", "urgency")
    search_fields = ("code", "notes")
    autocomplete_fields = ("registered_by", "approved_by")
