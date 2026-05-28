from django.contrib import admin
from .models import DataSource, EmissionRecord, AuditLog

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'client_name', 'uploaded_at']
    list_filter  = ['source_type']

@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display  = ['id', 'activity_description', 'quantity', 'unit', 'co2e_kg', 'scope', 'status', 'is_suspicious']
    list_filter   = ['status', 'scope', 'source__source_type', 'is_suspicious']
    search_fields = ['activity_description']
    readonly_fields = ['raw_data', 'approved_at']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['record', 'action', 'note', 'timestamp']