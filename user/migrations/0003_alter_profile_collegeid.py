# Generated by Django 4.1.5 on 2023-03-30 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_name_alter_user_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='collegeID',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
