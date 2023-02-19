
import json
import responses

from django.test import TestCase
from leaderboard.graphql import get_player_information, BASE_URL

class GraphQLTestCase(TestCase):

    def mock_graphql_response(self, response_data):
        """
        Mock the GraphQL API response for the get_player_information function
        """
        response_data_str = json.dumps(response_data)
        responses.add(
            responses.POST,
            BASE_URL,
            body=response_data_str,
            status=200,
            content_type='application/json'
        )
    
    @responses.activate
    def test_get_player_information(self):
        # Define the response data to mock
        mock_response_data = {
            'data': {
                'getConnectCode': {
                    'user': {
                        'rankedNetplayProfile': {
                            'wins': 10,
                            'losses': 5,
                            'ratingOrdinal': 1500,
                            'characters': {'fox': 3, 'falco': 1},
                        }
                    }
                }
            }
        }

        self.mock_graphql_response(mock_response_data)

        tag = 'IW2Z#1234'
        result = get_player_information(tag)
        # Check that the response is what we expected
        self.assertEqual(result, mock_response_data['data'])
