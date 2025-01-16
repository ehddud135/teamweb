from django.db import models

# Create your models here.


class Devices(models.Model):
    os_list = [('Android', 'android'), ('iOS', 'ios'), ('Unknown', 'unknown')]
    number = models.CharField(max_length=100)
    os = models.CharField(max_length=20, choices=os_list, default='Unknown')
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    architecture = models.CharField(max_length=20)
    rooting = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'Devices'
