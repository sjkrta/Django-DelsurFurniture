# Generated by Django 4.0.4 on 2022-05-31 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_order_shippingprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_choice',
            field=models.CharField(choices=[('P', 'Pick Up'), ('D', 'Delivered')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Canceled'), ('D', 'Delivered')], default='P', max_length=1),
        ),
    ]
