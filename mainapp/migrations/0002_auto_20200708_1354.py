# Generated by Django 2.2 on 2020-07-08 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gamecategory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
