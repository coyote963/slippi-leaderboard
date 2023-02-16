from django.core.management.base import BaseCommand, CommandError
from leaderboard.models import AccountUpdate, Account
from leaderboard.graphql import get_player_information

class Command(BaseCommand):
    help = 'Update accounts with new slippi data'

    def handle(self, *args, **options):
        for account in Account.objects.all():
            slippi_data = get_player_information(account.slippi_tag)
            new_update = AccountUpdate(
                account=account,
                slippi_data=slippi_data
            )
            new_update.save()
            account.last_updated = new_update.updated_on
