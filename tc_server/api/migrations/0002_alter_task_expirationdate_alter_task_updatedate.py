# Generated by Django 5.1.7 on 2025-03-27 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='expirationDate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='updateDate',
            field=models.DateTimeField(blank=True),
        ),
    ]
