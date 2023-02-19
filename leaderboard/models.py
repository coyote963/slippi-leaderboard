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
        unique=True,
        validators=[
            RegexValidator(
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
    
    display_name = models.CharField(
        max_length=40,
    )
    current_update = models.ForeignKey(
        'Update',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    previous_update = models.ForeignKey(
        'Update',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.slippi_tag

class Update(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='+')
    rating = models.FloatField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    characters = models.JSONField()
    ranking = models.IntegerField(blank=True)