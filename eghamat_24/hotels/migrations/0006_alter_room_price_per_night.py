# Generated by Django 5.1.3 on 2024-12-01 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_alter_hotel_city_alter_review_rating_delete_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='price_per_night',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
