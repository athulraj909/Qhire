# Generated by Django 5.1 on 2024-09-18 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='resume',
            field=models.FileField(upload_to='media'),
        ),
    ]
