# Generated by Django 5.0.1 on 2024-11-11 08:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditoriaUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tabla', models.CharField(max_length=100, verbose_name='Tabla')),
                ('registroid', models.IntegerField(verbose_name='Registro ID')),
                ('accion', models.CharField(choices=[('A', 'A'), ('M', 'M'), ('E', 'E')], max_length=10, verbose_name='Accion')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('hora', models.TimeField(verbose_name='Hora')),
                ('estacion', models.CharField(max_length=100, verbose_name='Estación')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Login.usuario', verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Auditoria Usuario',
                'verbose_name_plural': 'Auditorias Usuarios',
                'ordering': ('-fecha', 'hora'),
            },
        ),
    ]
