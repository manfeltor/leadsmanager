# Generated by Django 5.1.1 on 2024-09-21 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("usersapp", "0003_remove_customuser_mail"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "contact_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="userattribute",
            name="value1",
        ),
        migrations.RemoveField(
            model_name="userattribute",
            name="value2",
        ),
        migrations.AddField(
            model_name="userattribute",
            name="relacion",
            field=models.CharField(
                choices=[("empleado", "Empleado"), ("cliente", "Cliente")],
                default="empleado",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="usersapp.company",
            ),
        ),
        migrations.AddField(
            model_name="userattribute",
            name="comp",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_attributes",
                to="usersapp.company",
            ),
        ),
    ]
