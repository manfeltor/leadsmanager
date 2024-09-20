# Generated by Django 5.1.1 on 2024-09-19 23:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kpisapp", "0002_rename_delivery_simpliroutedata"),
    ]

    operations = [
        migrations.CreateModel(
            name="OmsData",
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
                ("pedido", models.CharField(max_length=50)),
                ("flujo", models.CharField(max_length=5)),
                ("seller", models.CharField(max_length=50)),
                ("sucCodigo", models.CharField(max_length=50)),
                ("sucursal", models.CharField(max_length=10)),
                ("estadoPedido", models.CharField(max_length=50)),
                ("fechaCreacion", models.DateTimeField()),
                ("fechaDespacho", models.DateTimeField(blank=True, null=True)),
                ("fechaEntrega", models.DateTimeField(blank=True, null=True)),
                ("lpn", models.CharField(max_length=30)),
                ("estadoLpn", models.CharField(max_length=50)),
                ("zona", models.CharField(max_length=50)),
                ("transporte", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "trackingColecta",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "trackingDistribucion",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "trackingTransporte",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("fechaRecepcion", models.DateTimeField(blank=True, null=True)),
                ("tipo", models.CharField(blank=True, max_length=50, null=True)),
                ("codigoPostal", models.CharField(max_length=20)),
                ("tte", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "tteSucursalDistribucion",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "tiendaEntrega",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
        ),
    ]