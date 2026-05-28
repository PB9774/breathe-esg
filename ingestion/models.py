from django.db import models

class DataSource(models.Model):
    SOURCE_TYPES = [
        ('SAP', 'SAP Fuel/Procurement'),
        ('UTILITY', 'Utility Electricity'),
        ('TRAVEL', 'Corporate Travel'),
    ]
    name = models.CharField(max_length=200)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    client_name = models.CharField(max_length=200)  # multi-tenancy
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_file = models.FileField(upload_to='uploads/')

class EmissionRecord(models.Model):
    SCOPE_CHOICES = [
        (1, 'Scope 1'),
        (2, 'Scope 2'),
        (3, 'Scope 3'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('flagged', 'Flagged'),
    ]
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    raw_data = models.JSONField()            # original row as-is
    activity_description = models.CharField(max_length=500)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)  # normalized to kWh or kg
    co2e_kg = models.FloatField()
    scope = models.IntegerField(choices=SCOPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_suspicious = models.BooleanField(default=False)
    suspicious_reason = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    edited = models.BooleanField(default=False)

class AuditLog(models.Model):
    record = models.ForeignKey(EmissionRecord, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)   # e.g. "approved", "flagged"
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)