# Generated by Django 4.1.4 on 2023-01-16 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_post_image_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='images/male.png', null=True, upload_to='images/'),
        ),
    ]