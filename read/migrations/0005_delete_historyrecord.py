# Generated by Django 3.1.6 on 2021-03-25 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0004_auto_20210325_0824'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoryRecord',
        ),
    ]