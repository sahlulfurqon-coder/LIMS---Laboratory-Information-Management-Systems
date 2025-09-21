from django.contrib import admin
from .models import Sample, SampleType


@admin.register(SampleType)
class SampleTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "code", "type", "subtype", "requester",
        "registered_by", "registered_at", "status", "urgency"
    )
    list_filter = ("status", "urgency", "type")
    search_fields = ("code", "requester", "notes")
