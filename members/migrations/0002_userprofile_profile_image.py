# Generated by Django 3.1.6 on 2021-03-25 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='', upload_to='profile/image', verbose_name='Profile Image'),
        ),
    ]