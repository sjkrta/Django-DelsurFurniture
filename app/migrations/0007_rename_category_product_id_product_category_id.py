# Generated by Django 4.0.4 on 2022-05-29 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_product_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category_product_id',
            new_name='category_id',
        ),
    ]
