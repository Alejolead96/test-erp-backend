from rest_framework import serializers
from documents.models import ValidationStep


class ValidationStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationStep
        fields = ['id','order','approver_user_id','validation_flow_id','status']
        read_only_fields = ['id','validation_flow_id']
