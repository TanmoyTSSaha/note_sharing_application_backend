# Generated by Django 4.1.5 on 2023-04-01 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user_profile_id',
        ),
    ]
