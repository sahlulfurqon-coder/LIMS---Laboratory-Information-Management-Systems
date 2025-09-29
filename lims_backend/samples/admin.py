from django.contrib import admin
from .models import Sample, SampleType, RawMaterial, FatBlend, Packaging, FinishedProduct


@admin.register(SampleType)
class SampleTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "description")
    search_fields = ("name", "category")


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "code", "type", "subtype",
        "tank", "registered_by", "registered_at",
        "status", "urgency",
    )
    list_filter = ("status", "urgency", "type", "tank")
    search_fields = ("code", "notes")
    autocomplete_fields = ("type", "detail", "registered_by", "approved_by")


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "variant", "type", "editable")
    list_filter = ("type", "editable")
    search_fields = ("name", "variant")


@admin.register(FatBlend)
class FatBlendAdmin(admin.ModelAdmin):
    list_display = ("id", "fatblend", "raw_material", "percentage")
    list_filter = ("raw_material",)
    search_fields = ("fatblend__code", "raw_material__name")


@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "editable")
    search_fields = ("name",)


@admin.register(FinishedProduct)
class FinishedProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "batch_code", "fatblend", "packaging", "created_at")
    list_filter = ("packaging",)
    search_fields = ("name", "batch_code")


