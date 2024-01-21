# Generated by Django 5.0.1 on 2024-01-21 08:50

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0006_reply_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo_field',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='images/'),
        ),
    ]