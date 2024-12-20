# Generated by Django 5.0.1 on 2024-11-08 10:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(max_length=50, unique=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.CharField(max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('numero_telefono', models.CharField(max_length=10, unique=True)),
                ('fecha_nacimiento', models.DateField()),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=10)),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('clave', models.CharField(max_length=128)),
                ('reset_token', models.CharField(blank=True, max_length=100, null=True)),
                ('reset_token_used', models.BooleanField(default=False)),
                ('ultimo_inicio_sesion', models.DateTimeField(blank=True, null=True)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Login.rol')),
            ],
            options={
                'verbose_name_plural': 'Usuarios',
            },
        ),
    ]
