# Generated by Django 5.1.1 on 2024-09-26 02:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

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
        migrations.CreateModel(
            name="SimpliRouteData",
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
                ("api_id", models.BigIntegerField(unique=True)),
                ("tracking_id", models.CharField(max_length=50, unique=True)),
                ("status", models.CharField(max_length=50)),
                ("title", models.CharField(max_length=255)),
                ("reference", models.CharField(blank=True, max_length=255, null=True)),
                ("planned_date", models.DateField()),
                ("programmed_date", models.DateField(blank=True, null=True)),
                ("created", models.DateTimeField()),
                ("visit_type", models.CharField(blank=True, max_length=50, null=True)),
                ("vehicle", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "checkout_observation",
                    models.CharField(
                        choices=[
                            (
                                "1068d8b8-f939-46f7-8819-6ab130329ce9",
                                "Fuera de ruta asignada",
                            ),
                            ("b068cd31-74c3-4f36-b60a-5f0a7b8837dd", "Entregado"),
                            ("e1b34560-430b-450d-a4df-55066d09172d", "Colectado"),
                            ("90fce0c5-4271-40f3-9f4f-71a6e3ee6e23", "Ausente"),
                            (
                                "c689bc80-a295-458e-a858-1251afc1925c",
                                "Devolución Cliente",
                            ),
                            (
                                "1190098c-5ae2-467f-9ff8-ab839ac0555a",
                                "Domicilio Incorrecto",
                            ),
                            ("4ae3ce34-2dc2-4a23-935b-93a7b0001875", "Cancelado"),
                            (
                                "9e4619d2-240f-4efb-bc73-f91e9469cd91",
                                "Mercaderia no despachada",
                            ),
                            ("d608375c-23cd-4ea3-bce8-25bfacc74ede", "Zona peligrosa"),
                            ("b77cf748-cd66-4c33-bdac-4b2ab0534b2b", "Rechazado"),
                            ("1a10310b-e710-4d66-8153-44ca9a88a8dc", "No Colectado"),
                            (
                                "853eaa3c-c265-4c4d-96ef-95fe580114fe",
                                "Demoras Operativas",
                            ),
                        ],
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderTrackingRelation",
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
                (
                    "oms_data",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="kpisapp.omsdata",
                    ),
                ),
                (
                    "simpli_route_data",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="kpisapp.simpliroutedata",
                    ),
                ),
            ],
        ),
    ]
