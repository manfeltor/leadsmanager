# Generated by Django 5.0.4 on 2024-08-14 17:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formsapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='formsubmission',
            name='assigned_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='formsubmission',
            name='management_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
