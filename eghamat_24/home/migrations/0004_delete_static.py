# Generated by Django 5.1.3 on 2024-11-19 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_hotel_city_remove_room_hotel_and_more'),
        ('hotels', '0002_city_alter_hotel_city'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Static',
        ),
    ]
