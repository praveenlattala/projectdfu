# Generated by Django 3.2 on 2022-10-25 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diabetes',
            name='pestimg',
            field=models.FileField(upload_to='app\\static\\diabetes'),
        ),
    ]
