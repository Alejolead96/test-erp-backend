from rest_framework import serializers
from documents.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'name', 'mime_type', 'size_bytes',
            'bucket_key', 'created_at', 'updated_at',
            'status', 'company', 'business_entity'
        ]
        read_only_fields = [
            'id', 'name', 'mime_type', 'size_bytes',
            'bucket_key', 'created_at', 'updated_at', 'status'
        ]
