# Generated by Django 5.0.4 on 2024-08-22 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formsapp', '0002_formsubmission_assigned_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsubmission',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('faltaCotizar', 'Falta cotizar'), ('cotizado', 'Cotizado'), ('interezadoAvanzar', 'Interesados en avanzar'), ('gestionExitosa', 'Gestion exitosa'), ('pospuesto', 'pospuesto'), ('noAvanzo', 'No avanzo'), ('noViable', 'No viable'), ('nuevoCliente', 'Nuevo cliente'), ('negativo', 'Negativo')], default='pendiente', max_length=50),
        ),
    ]