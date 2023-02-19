
from django.test import TestCase, Client
from leaderboard.models import Account, Update
from django.urls import reverse

from unittest.mock import patch
from leaderboard.management.commands.update_accounts import Command
from .utils import generic_api_response
from leaderboard.views import generate_rankings_table

class AccountTableViewTestCase(TestCase):

    def setUp(self):
        # Create some test data
        acc1 = Account.objects.create(slippi_tag='p#1', display_name='p1', approved=True)
        acc2 = Account.objects.create(slippi_tag='p#2', display_name='p2', approved=True)
        acc3 = Account.objects.create(slippi_tag='p#3', display_name='p3', approved=True)
        acc4 = Account.objects.create(slippi_tag='p#4', display_name='p4', approved=True)

        up1 = Update.objects.create(account=Account.objects.get(slippi_tag='p#1'), rating=1500, wins=10, losses=5, characters={'fox': 3, 'falco': 1}, ranking=1) 
        up2 = Update.objects.create(account=Account.objects.get(slippi_tag='p#2'), rating=1400, wins=5, losses=10, characters={'marth': 2, 'fox': 1}, ranking=2)
        up3 = Update.objects.create(account=Account.objects.get(slippi_tag='p#3'), rating=1300, wins=3, losses=7, characters={'puff': 1, 'peach': 1}, ranking=3)
        up4 = Update.objects.create(account=Account.objects.get(slippi_tag='p#4'), rating=1200, wins=3, losses=7, characters={'puff': 1, 'peach': 1}, ranking=4)


        pup1 = Update.objects.create(account=Account.objects.get(slippi_tag='p#1'), rating=900, wins=10, losses=5, characters={'fox': 3, 'falco': 1}, ranking=3) 
        pup2 = Update.objects.create(account=Account.objects.get(slippi_tag='p#2'), rating=1000, wins=5, losses=10, characters={'marth': 2, 'fox': 1}, ranking=2)
        pup3 = Update.objects.create(account=Account.objects.get(slippi_tag='p#3'), rating=1100, wins=3, losses=7, characters={'puff': 1, 'peach': 1}, ranking=1)


        acc1.current_update = up1
        acc2.current_update = up2
        acc3.current_update = up3
        acc4.current_update = up4

        acc1.previous_update = pup1
        acc2.previous_update = pup2
        acc3.previous_update = pup3

        acc1.save()
        acc2.save()        
        acc3.save()
        acc4.save()

        up1.save()
        up2.save()        
        up3.save()

        pup1.save()
        pup2.save()        
        pup3.save()
        
        

    def test_generate_rankings_table(self):
       
        rankings_table = generate_rankings_table()
        acc1 = Account.objects.get(slippi_tag='p#1')
        acc4 = Account.objects.get(slippi_tag='p#4')

        self.assertEqual(
            rankings_table[0],
            {
                'slippi_tag': acc1.slippi_tag,
                'display_name': acc1.display_name,
                'current_rating': acc1.current_update.rating,
                'current_ranking': acc1.current_update.ranking,
                'ranking_change': 2
            }
        )

        self.assertEqual(
            rankings_table[-1],
            {
                'slippi_tag': acc4.slippi_tag,
                'display_name': acc4.display_name,
                'current_rating': acc4.current_update.rating,
                'current_ranking': acc4.current_update.ranking,
                'ranking_change': 0
            }
        )

        self.assertEqual(
            acc4.previous_update,
            None
        )