# Generated by Django 4.2.1 on 2023-05-13 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_userprofile_age_userprofile_civil_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mobile_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]