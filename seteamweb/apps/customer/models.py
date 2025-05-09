import uuid
from django.db import models
from ..manager.models import Manager
from ..utils.utils import validate_year_month

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(Manager, to_field="name", on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    inspection = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'Customer'


class InstallationRecord(models.Model):
    customer = models.ForeignKey(Customer, to_field="name", on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, to_field="name", on_delete=models.SET_NULL, null=True)
    installation_date = models.DateField(null=False)
    significant = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'InstallationRecord'
        unique_together = ['customer', 'installation_date']


class InstallationCert(models.Model):
    record = models.ForeignKey(InstallationRecord, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'InstallationCert'

    def save(self, *args, **kwargs):
        if self.file:
            ext = self.file.name.split('.')[-1]
            new_name = f"{uuid.uuid4().hex}.{ext}"
            self.file.name = new_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
