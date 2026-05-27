from django.db import models
import json


class Tenant(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Source(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=50)
    filename = models.CharField(max_length=255, null=True, blank=True)
    ingested_at = models.DateTimeField(auto_now_add=True)
    raw_payload = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.tenant} - {self.source_type}"


class EmissionRecord(models.Model):
    STATUS_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('locked', 'Locked'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    source_row_id = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=100)
    scope = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    normalized_amount_kgco2e = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    normalized_unit = models.CharField(max_length=50, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending_review')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.category} {self.amount} {self.unit}"


class AuditLog(models.Model):
    emission_record = models.ForeignKey(EmissionRecord, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=100)
    performed_by = models.CharField(max_length=200, null=True, blank=True)
    performed_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Audit {self.action} on {self.emission_record_id} by {self.performed_by}"
