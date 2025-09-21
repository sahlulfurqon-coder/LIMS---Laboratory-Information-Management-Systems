from rest_framework import serializers
from .models import Complaint, CAPA

class CAPASerializer(serializers.ModelSerializer):
    class Meta:
        model = CAPA
        fields = "__all__"

class ComplaintSerializer(serializers.ModelSerializer):
    capa_details = CAPASerializer(many=True, read_only=True)

    class Meta:
        model = Complaint
        fields = "__all__"
