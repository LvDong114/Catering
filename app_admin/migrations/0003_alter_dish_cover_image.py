# Generated by Django 4.2.16 on 2025-02-04 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0002_dish_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='cover_image',
            field=models.ImageField(upload_to=''),
        ),
    ]
