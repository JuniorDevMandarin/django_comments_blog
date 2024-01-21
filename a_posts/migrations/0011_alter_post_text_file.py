# Generated by Django 5.0.1 on 2024-01-21 14:04

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0010_alter_post_photo_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text_file',
            field=models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='files/'),
        ),
    ]