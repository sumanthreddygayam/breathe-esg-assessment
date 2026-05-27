from django.contrib import admin
from .models import Tenant, Source, EmissionRecord
from .models import AuditLog

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'source_type', 'filename', 'ingested_at')


@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'category', 'amount', 'unit', 'status', 'created_at')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'emission_record', 'action', 'performed_by', 'performed_at')
