# Generated by Django 4.1.7 on 2023-02-18 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0006_alter_account_slippi_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountupdate',
            name='slippi_data',
        ),
        migrations.AddField(
            model_name='account',
            name='display_name',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountupdate',
            name='characters',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountupdate',
            name='losses',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountupdate',
            name='rating',
            field=models.FloatField(default=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountupdate',
            name='wins',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
