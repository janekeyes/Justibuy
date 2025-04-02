# Generated by Django 4.2.10 on 2025-03-26 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User Profile'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(db_index=True, max_length=150, unique=True),
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='user_profiles',
        ),
    ]
