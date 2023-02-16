from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from .graphql import connect_code_exists

def validate_slippi_tag(value):
    if not connect_code_exists(value):
        raise ValidationError('Slippi Tag not found')

class Account(models.Model):
    slippi_tag = models.CharField(
        'Slippi Tag to register',
        max_length=40,
        validators=[RegexValidator(
            regex='^[A-Z0-9]{1,8}#[0-9]{1,4}$',
            message='''Invalid Slippi Tag. 
                Must be up to 8 Alphanumerals 
                followed by a "#" and up to 4 digits''',
            code='invalid_slippi_tag'
        ),
        validate_slippi_tag
        ]
    )
    approved = models.BooleanField(
        'Whether tag is approved',
        default=False
    )
    last_updated = models.DateTimeField(
        'Last time the rank information was refreshed',
        auto_now_add=True,
        blank=True
    )
