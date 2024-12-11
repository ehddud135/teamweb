from django.db import models
from ..customer.models import Customer

# Create your models here.


class Packages(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=25)  # 'Android' or 'iOS'
    license_expire_date = models.DateField(blank=True, null=True)
    customer = models.ForeignKey(Customer, to_field="name", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Packages'
        unique_together = ['name', 'platform']


class AndroidApplyOptions(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    check_root = models.BooleanField(default=False)
    detect_magisk = models.BooleanField(default=False)
    check_integrity = models.BooleanField(default=False)
    check_emul = models.BooleanField(default=False)
    check_debugging = models.BooleanField(default=False)
    prevent_debugging = models.BooleanField(default=False)
    prevent_adb = models.BooleanField(default=False)
    encrypt_so = models.BooleanField(default=False)
    self_protect = models.BooleanField(default=False)
    prevent_decompile = models.BooleanField(default=False)
    chekc_mem_scanner = models.BooleanField(default=False)
    encrypt_flutter = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'AndroidApplyOptions'


class iOSApplyOptions(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    objc_string_encryption = models.BooleanField(default=False)
    swift_string_encryption = models.BooleanField(default=False)
    jailbreak_check = models.BooleanField(default=False)
    threat_check = models.BooleanField(default=False)
    integrity_check = models.BooleanField(default=False)
    flex_3_check = models.BooleanField(default=False)
    server_auth_manually = models.BooleanField(default=False)
    objc_obfuscate = models.BooleanField(default=False)
    swift_obfuscate = models.BooleanField(default=False)
    symbol_delete = models.BooleanField(default=False)
    log_hiding = models.BooleanField(default=False)
    dynamic_api_hiding = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'iOSApplyOptions'
