# Generated by Django 5.1.5 on 2025-04-08 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliquepay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
