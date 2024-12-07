# Generated by Django 5.1.3 on 2024-12-03 07:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userprofile_first_name_userprofile_last_name_and_more'),
        ('reservations', '0007_paymentinfo_tracking_code_reservation_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentinfo',
            name='discount_price',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='قیمت با تخفیف'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='accounts.userprofile'),
        ),
    ]