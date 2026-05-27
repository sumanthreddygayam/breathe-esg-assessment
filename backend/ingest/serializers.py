from rest_framework import serializers
from .models import Tenant, Source, EmissionRecord


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class EmissionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionRecord
        fields = '__all__'
        read_only_fields = ('id', 'tenant', 'source', 'created_at', 'updated_at')
