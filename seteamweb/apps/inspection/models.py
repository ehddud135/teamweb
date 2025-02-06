from django.db import models
from django.core.exceptions import ValidationError
from ..packages.models import Packages
from ..customer.models import Customer
from ..devices.models import Devices
from ..utils.utils import validate_year_month
import uuid


# Create your models here.


class AndroidInspectResult(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    app_name = models.CharField(null=True, default="Unknown", max_length=30)
    app_version = models.CharField(null=True, default="Unknown", max_length=30)
    rooting_test = models.BooleanField(default=False)
    rooting = models.BooleanField(default=False)
    integrity = models.BooleanField(default=False)
    emulator = models.BooleanField(default=False)
    obfuscate = models.BooleanField(default=False)
    decompile = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'AndroidInspectResult'


class iOSInspectResult(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    app_name = models.CharField(null=True, default="Unknown", max_length=30)
    app_version = models.CharField(null=True, default="Unknown", max_length=30)
    jailbreak_test = models.BooleanField(default=False)
    jailbreak = models.BooleanField(default=False)
    integrity = models.BooleanField(default=False)
    string_encrypt = models.BooleanField(default=False)
    symbol_del = models.BooleanField(default=False)
    library_version = models.CharField(max_length=30, default="Unknown")
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'iOSInspectResult'


class InspectionRecord(models.Model):
    result_list = [('incomplete', 'Incomplete'), ('complete', 'Complete')]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inspection_month = models.CharField(max_length=7, validators=[validate_year_month])
    inspection_date = models.DateField(null=True)
    result = models.CharField(max_length=15, choices=result_list, default='incomplete')
    details = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'InspectionRecord'
        unique_together = ['customer', 'inspection_month']


class InspectionSchedule(models.Model):
    Period_list = [
        ('monthly', 'Monthly'), ('quarter', 'Quarter'), ('half', 'Half'), ('undecided', 'Undecided')
    ]
    name = models.ForeignKey(Customer, to_field="name", on_delete=models.CASCADE)
    Period = models.CharField(max_length=25, choices=Period_list, default='undecided')
    January = models.BooleanField(default=False)
    February = models.BooleanField(default=False)
    March = models.BooleanField(default=False)
    April = models.BooleanField(default=False)
    May = models.BooleanField(default=False)
    June = models.BooleanField(default=False)
    July = models.BooleanField(default=False)
    August = models.BooleanField(default=False)
    September = models.BooleanField(default=False)
    October = models.BooleanField(default=False)
    November = models.BooleanField(default=False)
    December = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'InspectionSchedule'


class InspectionResultFile(models.Model):
    inspectrecord = models.ForeignKey(InspectionRecord, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file:
            ext = self.file.name.split('.')[-1]
            new_name = f"{uuid.uuid4().hex}.{ext}"
            self.file.name = new_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
