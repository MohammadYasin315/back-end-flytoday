# Generated by Django 5.1.3 on 2024-12-14 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0007_alter_hotel_facilities_alter_hotel_faqs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='facilities',
            field=models.TextField(default=list),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='faqs',
            field=models.TextField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='restaurants_and_cafes',
            field=models.TextField(default=list),
        ),
    ]
