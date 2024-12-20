# Generated by Django 5.0.1 on 2024-11-26 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submodulos', '0004_alter_estadistica_estadistica'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='puestocualidad',
            options={'verbose_name_plural': 'Puestos - Cualidades'},
        ),
        migrations.AlterField(
            model_name='estadistica',
            name='estadistica',
            field=models.CharField(choices=[('TIROS TOTALES', 'TIROS TOTALES'), ('TIROS AL ARCO', 'TIROS AL ARCO'), ('GOLES ANOTADOS', 'GOLES ANOTADOS'), ('PENALES EJECUTADOS', 'PENALES EJECUTADOS'), ('PENALES ANOTADOS', 'PENALES ANOTADOS'), ('PASES TOTALES', 'PASES TOTALES'), ('PASES ACERTADOS', 'PASES ACERTADOS'), ('CENTROS TOTALES', 'CENTROS TOTALES'), ('CENTROS ACERTADOS', 'CENTROS ACERTADOS'), ('SPRINT', 'SPRINT'), ('ACELERACION', 'ACELERACION'), ('REGATES TOTALES', 'REGATES TOTALES'), ('REGATES EXITOSOS', 'REGATES EXITOSOS'), ('DUELOS TOTALES', 'DUELOS TOTALES'), ('DUELOS EXITOSOS', 'DUELOS EXITOSOS'), ('INTERCEPCIONES INTENTOS', 'INTERCEPCIONES INTENTOS'), ('INTERCEPCIONES EXITOSAS', 'INTERCEPCIONES EXITOSAS'), ('DUELOS DEFENSIVOS TOTALES', 'DUELOS DEFENSIVOS TOTALES'), ('DUELOS DEFENSIVOS GANADOS', 'DUELOS DEFENSIVOS GANADOS'), ('SALTO EVALUADO', 'SALTO EVALUADO'), ('DISTANCIA RECORRIDA', 'DISTANCIA RECORRIDA'), ('SPRINTS REALIZADOS', 'SPRINTS REALIZADOS'), ('FUERZA EXPLOSIVA EVALUADA', 'FUERZA EXPLOSIVA EVALUADA'), ('FUERZA ISOMETRICA EVALUADA', 'FUERZA ISOMETRICA EVALUADA'), ('FUERZA RESISTENCIA EVALUADA', 'FUERZA RESISTENCIA EVALUADA'), ('TIROS TOTALES RECIBIDOS', 'TIROS TOTALES'), ('TIROS BLOQUEADOS MANEJO', 'TIROS BLOQUEADOS'), ('DESPEJES TOTALES', 'DESPEJES TOTALES'), ('DESPEJES EXITOSOS', 'DESPEJES EXITOSOS'), ('BALONES ATRAPADOS', 'BALONES ATRAPADOS'), ('ATRAPES SIN REBOTE', 'ATRAPES SIN REBOTE'), ('PENALES RECIBIDOS', 'PENALES RECIBIDOS'), ('PENALES ATAJADOS', 'PENALES ATAJADOS'), ('1V1 TOTALES', '1V1 TOTALES'), ('1V1 GANADOS', '1V1 GANADOS'), ('TIROS BLOQUEADOS REFLEJOS', 'TIROS BLOQUEADOS'), ('ATAJADAS CRITICAS REFLEJOS', 'ATAJADAS CRITICAS'), ('SAQUES LARGOS INTENTOS', 'SAQUES LARGOS INTENTOS'), ('SAQUES LARGOS EXITOSOS', 'SAQUES LARGOS EXITOSOS'), ('SAQUES CORTOS INTENTOS', 'SAQUES CORTOS INTENTOS'), ('SAQUES CORTOS EXITOSOS', 'SAQUES CORTOS EXITOSOS')], max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='puestocualidad',
            name='puesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='puesto_cualidades', to='submodulos.puesto'),
        ),
    ]
