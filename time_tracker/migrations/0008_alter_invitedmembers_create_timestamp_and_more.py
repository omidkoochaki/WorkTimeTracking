# Generated by Django 4.1 on 2022-09-06 14:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('time_tracker', '0007_alter_invitedmembers_create_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitedmembers',
            name='create_timestamp',
            field=models.FloatField(default=1662476368.577764),
        ),
        migrations.AlterField(
            model_name='project',
            name='create_timestamp',
            field=models.FloatField(default=1662476368.577764),
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projectdailyreporting',
            name='create_timestamp',
            field=models.FloatField(default=1662476368.577764),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_timestamp',
            field=models.FloatField(default=1662476368.577764),
        ),
        migrations.AlterField(
            model_name='taskdailyreporting',
            name='create_timestamp',
            field=models.FloatField(default=1662476368.577764),
        ),
        migrations.AlterField(
            model_name='worktimerecord',
            name='end_time',
            field=models.FloatField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='worktimerecord',
            name='start_time',
            field=models.FloatField(default=1662476368.578514),
        ),
    ]
