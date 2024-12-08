# Generated by Django 5.1.3 on 2024-12-08 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0011_alter_reservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinfo',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='قیمت با تخفیف'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('PENDING', 'در انتظار پرداخت'), ('SUCCESS', 'موفق')], default='PENDING', max_length=10, verbose_name='وضعیت رزرو'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='قیمت کل'),
        ),
    ]
