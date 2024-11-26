# Generated by Django 5.1.2 on 2024-11-26 11:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_productedithistory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='productedithistory',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productedithistory',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]