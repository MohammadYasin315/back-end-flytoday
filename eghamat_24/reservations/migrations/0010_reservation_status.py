# Generated by Django 5.1.3 on 2024-12-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0009_alter_reservation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'در انتظار پرداخت'), ('confirmed', 'تأیید شده'), ('cancelled', 'لغو شده')], default='pending', max_length=10, verbose_name='وضعیت رزرو'),
        ),
    ]
