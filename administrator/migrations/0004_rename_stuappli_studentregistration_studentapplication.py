# Generated by Django 3.2.1 on 2021-05-08 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_auto_20210508_0028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentregistration',
            old_name='stuappli',
            new_name='studentApplication',
        ),
    ]
