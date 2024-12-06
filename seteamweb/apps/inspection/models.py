from django.db import models
from ..packages.models import Packages
from ..customer.models import Customer

# Create your models here.


class AndroidInspectResult(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    device_info = models.CharField(max_length=30, blank=True, null=True)
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
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    device_info = models.CharField(max_length=30, blank=True, null=True)
    jailbreak_test = models.BooleanField(default=False)
    jailbreak = models.BooleanField(default=False)
    integrity = models.BooleanField(default=False)
    string_encrypt = models.BooleanField(default=False)
    symbol_del = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'iOSInspectResult'


class InspectionRecord(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    inspection_date = models.DateField()
    details = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'InspectionRecord'


class InspectionSchedule(models.Model):
    name = models.ForeignKey(Customer, to_field="name", on_delete=models.CASCADE)
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
