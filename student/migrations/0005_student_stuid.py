# Generated by Django 3.2.1 on 2021-05-06 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_student_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='stuid',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
