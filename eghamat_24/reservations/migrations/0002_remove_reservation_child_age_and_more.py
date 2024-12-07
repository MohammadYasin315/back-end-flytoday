# Generated by Django 5.1.3 on 2024-11-30 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='child_age',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='children',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
