# Generated by Django 3.2 on 2021-04-22 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_student_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.PositiveSmallIntegerField(verbose_name='group'),
        ),
    ]
