from django.db import models


class Account(models.Model):
    slippi_tag = models.CharField(
        'Slippi Tag to register',
        max_length=40)
    approved = models.BooleanField(
        'Whether tag is approved',
        default=True
    )
    alternate_name = models.CharField(
        'Alternative name to display',
        max_length=40
    )
    last_updated = models.DateTimeField(
        'Last time the rank information was refreshed'
    )
