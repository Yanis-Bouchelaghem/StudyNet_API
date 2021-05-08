# Generated by Django 3.2 on 2021-05-08 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Management', '0001_initial'),
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.department', verbose_name='department'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='sections',
            field=models.ManyToManyField(through='Management.TeacherSection', to='Management.Section', verbose_name='sections'),
        ),
        migrations.AddField(
            model_name='student',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.section', verbose_name='section'),
        ),
    ]
