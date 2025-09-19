from rest_framework import serializers
from documents.models import ValidationFlow


class ValidationFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationFlow
        fields = ['id','enable','created_at']
        read_only_fields = ['id','created_at']
