# Generated by Django 2.0.6 on 2018-06-16 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortlink', '0005_auto_20180616_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='basic_link',
            field=models.CharField(max_length=256),
        ),
    ]
