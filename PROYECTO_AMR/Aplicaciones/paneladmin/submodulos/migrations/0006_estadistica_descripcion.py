# Generated by Django 5.0.1 on 2024-11-27 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submodulos', '0005_alter_puestocualidad_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='estadistica',
            name='descripcion',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
