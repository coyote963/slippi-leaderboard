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
            if 'wins' in ranked_profile and 'losses' in ranked_profile and 'ratingOrdinal' in ranked_profile:
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
            raise Exception("Data was improperly formatted")

        
    def commit_updates(all_updates):
        for idx, au in enumerate(sorted(
            all_updates,
            key=lambda x: x['update'].rating,
            reverse=True)):
            au['update'].ranking = idx + 1
            au['update'].save()
        
        for au in all_updates:
            account = au['account'] 
            account.previous_update = account.current_update
            account.current_update = au['update']
            account.save()


    def handle(self, *args, **options):
        all_updates = []
        for account in Account.objects.filter(approved=True):
            try:
                all_updates.append({
                    'update': Command.create_update(account),
                    'account': account
                })
            except Exception as err:
                logging.error(print(Exception, err))
        Command.commit_updates(all_updates)