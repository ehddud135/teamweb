from django.db import models
from ..manager.models import Manager

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(Manager, to_field="name", on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Customer'
