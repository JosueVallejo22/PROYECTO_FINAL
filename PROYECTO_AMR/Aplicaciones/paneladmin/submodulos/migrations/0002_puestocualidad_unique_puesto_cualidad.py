# Generated by Django 5.0.1 on 2024-11-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submodulos', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='puestocualidad',
            constraint=models.UniqueConstraint(fields=('puesto', 'cualidad'), name='unique_puesto_cualidad'),
        ),
    ]
