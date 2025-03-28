# Generated by Django 5.1.4 on 2025-01-16 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100)),
                ('os', models.CharField(choices=[('Android', 'android'), ('iOS', 'ios'), ('Unknown', 'unknown')], default='Unknown', max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=20)),
                ('architecture', models.CharField(max_length=20)),
                ('rooting', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Devices',
                'managed': True,
                'unique_together': {('number', 'os')},
            },
        ),
        migrations.DeleteModel(
            name='AndroidDevices',
        ),
        migrations.DeleteModel(
            name='iOSDevices',
        ),
    ]
