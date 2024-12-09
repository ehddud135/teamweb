from django.db import models

# Create your models here.


class Manager(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, default=None)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Manager'
