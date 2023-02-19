
from django.test import TestCase, Client
from leaderboard.models import Account, Update
from django.urls import reverse

from unittest.mock import patch
from leaderboard.management.commands.update_accounts import Command
from .utils import generic_api_response


class AccountTableViewTestCase(TestCase):

    def setUp(self):
        # Create some test data
        acc1 = Account.objects.create(slippi_tag='EXAMPLE1#1', display_name='Example 1', approved=True)
        acc2 = Account.objects.create(slippi_tag='EXAMPLE2#2', display_name='Example 2', approved=True)
        acc3 = Account.objects.create(slippi_tag='EXAMPLE3#3', display_name='Example 3', approved=True)
        acc4 = Account.objects.create(slippi_tag='EXAMPLE4#4', display_name='Example 4', approved=True)

        up1 = Update.objects.create(account=Account.objects.get(slippi_tag='EXAMPLE1#1'), rating=1500, wins=10, losses=5, characters={'fox': 3, 'falco': 1}, ranking=1) 
        up2 = Update.objects.create(account=Account.objects.get(slippi_tag='EXAMPLE2#2'), rating=1400, wins=5, losses=10, characters={'marth': 2, 'fox': 1}, ranking=2)
        up3 = Update.objects.create(account=Account.objects.get(slippi_tag='EXAMPLE3#3'), rating=1300, wins=3, losses=7, characters={'puff': 1, 'peach': 1}, ranking=3)
        up4 = Update.objects.create(account=Account.objects.get(slippi_tag='EXAMPLE3#3'), rating=2000, wins=3, losses=7, characters={'puff': 1, 'peach': 1}, ranking=3)
        up5 = Update.objects.create(account=Account.objects.get(slippi_tag='EXAMPLE3#3'), rating=2300, wins=3, losses=7, characters={'puff': 1, 'peach': 1}, ranking=3)


        acc1.current_update = up1
        acc2.current_update = up2
        acc3.current_update = up3
        acc4.current_update = up4
        acc4.previous_update = up5

        acc1.save()
        acc2.save()        
        acc3.save()
        acc4.save()
        
        up1.save()
        up2.save()        
        up3.save()
        up4.save()
        up5.save()

    @patch('leaderboard.management.commands.update_accounts.get_player_information')
    def test_integration_rankings_is_set_correctly(self, mock_method):
        def my_side_effect(slippi_tag):
            if slippi_tag == 'EXAMPLE4#4':
                return {'message': 'intentional invalid slippi response'}
            
            return {
                'EXAMPLE1#1': generic_api_response(1000),
                'EXAMPLE2#2': generic_api_response(1200),
                'EXAMPLE3#3': generic_api_response(0)
            }[slippi_tag]
        
        mock_method.side_effect = my_side_effect

        Command.update_accounts()

        account1 = Account.objects.get(slippi_tag='EXAMPLE1#1')
        account2 = Account.objects.get(slippi_tag='EXAMPLE2#2')
        account3 = Account.objects.get(slippi_tag='EXAMPLE3#3')
        account4 = Account.objects.get(slippi_tag='EXAMPLE4#4')


        self.assertEqual(account1.current_update.rating, 1000)
        self.assertEqual(account2.current_update.rating, 1200)
        self.assertEqual(account3.current_update.rating, 0)

        self.assertEqual(account1.previous_update.rating, 1500)
        self.assertEqual(account2.previous_update.rating, 1400)
        self.assertEqual(account3.previous_update.rating, 1300)

        self.assertEqual(account1.current_update.ranking, 2)
        self.assertEqual(account2.current_update.ranking, 1)
        self.assertEqual(account3.current_update.ranking, 3)

        self.assertEqual(account4.current_update, None)
        self.assertEqual(account4.previous_update, None)



        
  