# Generated by Django 4.0.4 on 2022-05-30 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_rename_color_color_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='product_id',
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, null=True, to='app.color'),
        ),
    ]
