# Generated by Django 4.2.10 on 2025-04-14 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_clothing_image_path_clothing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothing',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='clothing_images/'),
        ),
    ]
