# Generated by Django 3.2.1 on 2021-05-06 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('ssc_marks', models.IntegerField()),
                ('internal_marks', models.IntegerField()),
                ('mobile_no', models.IntegerField()),
                ('dept', models.CharField(max_length=255)),
                ('profile_pic', models.ImageField(upload_to='studentimages/')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('father_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]