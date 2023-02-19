from django.test import TestCase
from django.test import TestCase
from .management.commands.update_accounts import Command

class UpdateAccountValidationTestCase(TestCase):
    def test_is_valid_json_response_invalid_data(self):
        """Test if invalid slippi data result returns None"""
        result = Command.get_ranked_profile({})
        self.assertEqual(result, None)

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
                        "id":"0x2e083d",
                        "ratingOrdinal":1491.681666,
                        "ratingUpdateCount":79,
                        "wins":41,
                        "losses":38,
                        "dailyGlobalPlacement":"None",
                        "dailyRegionalPlacement":"None",
                        "continent":"NORTH_AMERICA",
                        "characters":[
                        {
                            "id":"0x35a6b1",
                            "character":"CAPTAIN_FALCON",
                            "gameCount":172
                        },
                        {
                            "id":"0x3618f0",
                            "character":"FOX",
                            "gameCount":7
                        },
                        {
                            "id":"0x372a7e",
                            "character":"FALCO",
                            "gameCount":1
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

