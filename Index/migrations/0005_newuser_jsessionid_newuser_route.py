# Generated by Django 4.1 on 2022-08-13 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0004_remove_newuser_jsessionid_remove_newuser_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='JSESSIONID',
            field=models.CharField(default=0, max_length=60, verbose_name='jes'),
        ),
        migrations.AddField(
            model_name='newuser',
            name='route',
            field=models.CharField(default=0, max_length=80, verbose_name='route'),
        ),
    ]