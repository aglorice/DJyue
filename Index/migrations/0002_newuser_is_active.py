# Generated by Django 4.1 on 2022-08-10 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='is_active',
            field=models.CharField(choices=[(1, 'True'), (0, 'False')], default=0, max_length=4, verbose_name='激活状态'),
        ),
    ]
