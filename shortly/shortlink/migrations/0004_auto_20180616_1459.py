# Generated by Django 2.0.6 on 2018-06-16 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortlink', '0003_auto_20180616_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='short_link',
            new_name='short_id',
        ),
    ]
