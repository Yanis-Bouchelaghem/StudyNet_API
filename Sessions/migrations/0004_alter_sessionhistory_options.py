# Generated by Django 3.2 on 2021-04-18 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sessions', '0003_auto_20210418_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessionhistory',
            options={'verbose_name': 'Session history', 'verbose_name_plural': 'Sessions history'},
        ),
    ]