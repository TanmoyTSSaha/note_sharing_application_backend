# Generated by Django 4.1.5 on 2023-04-01 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_collegeid_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_profile_id',
            field=models.IntegerField(default=0),
        ),
    ]
