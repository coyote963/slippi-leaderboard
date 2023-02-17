# Generated by Django 4.1.7 on 2023-02-17 03:32

import django.core.validators
from django.db import migrations, models
import leaderboard.models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0003_alter_account_slippi_tag_accountupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='slippi_tag',
            field=models.CharField(max_length=40, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_slippi_tag', message='Invalid Slippi Tag. \n                    Must be up to 8 Alphanumerals \n                    followed by a "#" and up to 4 digits', regex='^[A-Z0-9]{1,8}#[0-9]{1,4}$'), leaderboard.models.validate_slippi_tag], verbose_name='Slippi Tag to register'),
        ),
    ]
