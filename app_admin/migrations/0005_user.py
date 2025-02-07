# Generated by Django 4.2.16 on 2025-02-04 07:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0004_announcement_alter_dish_cover_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('nickname', models.CharField(max_length=128, verbose_name='昵称')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='手机号')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='注册时间')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['-date_joined'],
            },
        ),
    ]
