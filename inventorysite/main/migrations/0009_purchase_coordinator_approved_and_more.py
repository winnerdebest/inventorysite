# Generated by Django 5.1.2 on 2024-11-30 11:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_productedithistory_approved_by_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='coordinator_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='purchase',
            name='coordinator_approver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coordinator_approvals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchase',
            name='gm_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='purchase',
            name='gm_approver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gm_approvals', to=settings.AUTH_USER_MODEL),
        ),
    ]
