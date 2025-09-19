from rest_framework import serializers
from documents.models import BusinessEntity


class BusinessEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessEntity
        fields = ['id','entity_type','company','created_at']
        read_only_fields = ['id','created_at']