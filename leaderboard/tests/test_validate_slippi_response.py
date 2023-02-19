from django.test import TestCase
from leaderboard.management.commands.update_accounts import Command
from .utils import generic_api_response

class UpdateAccountValidationTestCase(TestCase):
    def test_is_valid_json_response_invalid_data(self):
        """Test if invalid slippi data result returns None"""
        result = Command.get_ranked_profile({})
        self.assertEqual(result, None)

    def test_generic_api_response(self):
        sample_slippi = generic_api_response(0)
        self.assertEqual(
            Command.get_ranked_profile(sample_slippi),
            sample_slippi['getConnectCode']['user']['rankedNetplayProfile']
        )

    def test_is_valid_json_response_valid_data(self):
        """Test get_ranked_profile with valid slippi data"""
        sample_slippi = {
            "getConnectCode":{
                "user":{
                    "displayName":"kitty",
                    "connectCode":{
                        "code":"JOHN#337"
                    },
                    "rankedNetplayProfile":{
                        "ratingOrdinal":1491.681666,
                        "ratingUpdateCount":79,
                        "wins":41,
                        "losses":38,
                        "characters":[
                        {
                            "id":"0x35a6b1",
                            "character":"CAPTAIN_FALCON",
                            "gameCount":172
                        },
                        {
                            "id":"0x635552",
                            "character":"NESS",
                            "gameCount":1
                        },
                        {
                            "id":"0x6358d4",
                            "character":"GAME_AND_WATCH",
                            "gameCount":1
                        }
                        ]
                    }
                }
            }
        }
        result = Command.get_ranked_profile(sample_slippi)

        self.assertEqual(result, sample_slippi['getConnectCode']['user']['rankedNetplayProfile'])

