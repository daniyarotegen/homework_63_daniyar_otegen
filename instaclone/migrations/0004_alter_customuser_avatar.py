# Generated by Django 4.1.7 on 2023-03-28 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instaclone', '0003_remove_customuser_following_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(upload_to='media/avatars/'),
        ),
    ]