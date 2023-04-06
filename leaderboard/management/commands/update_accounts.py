import logging

from django.core.management.base import BaseCommand, CommandError
from leaderboard.models import Update, Account
from leaderboard.graphql import get_player_information


class Command(BaseCommand):
    help = 'Update accounts with new slippi data'

    def get_ranked_profile(slippi_data):
        if 'getConnectCode' in slippi_data \
        and 'user' in slippi_data['getConnectCode'] \
        and 'rankedNetplayProfile' in slippi_data['getConnectCode']['user']:
            ranked_profile = slippi_data['getConnectCode']['user']['rankedNetplayProfile']
            if 'wins' in ranked_profile \
                and 'losses' in ranked_profile \
                and 'ratingOrdinal' in ranked_profile \
                and ranked_profile['wins'] is not None\
                and ranked_profile['losses'] is not None\
                and ranked_profile['ratingOrdinal'] is not None:
                return ranked_profile
        return None 


    def create_update(account):
        slippi_data = get_player_information(account.slippi_tag)
        ranked_profile = Command.get_ranked_profile(slippi_data)
        if ranked_profile:
            return Update(
                account=account,
                rating=ranked_profile['ratingOrdinal'],
                wins=ranked_profile['wins'],
                losses=ranked_profile['losses'],
                characters=ranked_profile['characters'],
                ranking=True
            )
        else:
            raise Exception(f"Invalid Slippi Response: {slippi_data}")

        
    def commit_updates(all_updates):
        for idx, au in enumerate(sorted(
            all_updates,
            key=lambda x: x['update'].rating,
            reverse=True)):
            update = au['update']
            update.ranking = idx + 1
            update.save()
        
        for au in all_updates:
            account = au['account'] 
            account.previous_update = account.current_update
            account.current_update = au['update']
            account.save()

    def clear_account_updates(account):
        account.current_update = None
        account.previous_update = None
        account.save()


    def update_accounts():
        all_updates = []
        for account in Account.objects.filter(approved=True):
            try:
                all_updates.append({
                    'update': Command.create_update(account),
                    'account': account
                })
            except Exception as err:
                Command.clear_account_updates(account)
                logging.error(err)
        Command.commit_updates(all_updates)


    def handle(self, *args, **options):
        Command.update_accounts()