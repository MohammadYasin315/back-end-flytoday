# Generated by Django 5.1.3 on 2024-12-15 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_alter_hotel_facilities_alter_hotel_faqs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='facilities',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='faqs',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='restaurants_and_cafes',
            field=models.TextField(),
        ),
    ]
