from datetime import date
from django.db import models
from apps.packages.models import Packages
from apps.utils.utils import validate_year_month

# Create your models here.

class AndroidResult(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE, limit_choices_to={"platform": "Android"})
    app_name = models.CharField(null=True, default="Unknown", max_length=30)
    app_version = models.CharField(null=True, default="Unknown", max_length=30)
    rooting = models.BooleanField(default=False)
    integrity = models.BooleanField(default=False)
    emulator = models.BooleanField(default=False)
    obfuscate = models.TextField(null=True, default="Unknown")
    momo_size = models.TextField(null=True, default="Unknown")
    decompile = models.BooleanField(default=False)
    inspection_month = models.CharField(max_length=7, validators=[validate_year_month], default=date.today().strftime("%Y-%m"))

    class Meta:
        managed = True
        db_table = 'AndroidResult'
        unique_together = ('package', 'inspection_month')
