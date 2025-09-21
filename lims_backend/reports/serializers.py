from rest_framework import serializers
from .models import AuditTrail
from samples.models import Sample
from complaints.models import Complaint
from specs.models import Specification
from requests.models import ExternalAnalysisResult

class SampleReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ['code','type','subtype','requester','registered_at','status','urgency']

class ComplaintReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['id','title','status','reported_by','assigned_to','created_at','capa']

class SpecsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['id','name','version','status','created_at','approved_by']

class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'

class ExternalAnalysisReportSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(source='request.id')
    requester = serializers.CharField(source='request.requester')

    class Meta:
        model = ExternalAnalysisResult
        fields = ['request_id', 'requester', 'sample_code', 'parameter', 'result', 'method', 'performed_by', 'completed_at']