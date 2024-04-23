# Generated by Django 5.0.4 on 2024-04-23 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0002_remove_plans_user_userplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userplan',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plans.plans'),
        ),
    ]
