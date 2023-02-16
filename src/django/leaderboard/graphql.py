import requests

BASE_URL = 'https://gql-gateway-dot-slippi.uc.r.appspot.com/graphql'

def get_player_information(connect_code: str, base_url=BASE_URL):
    '''Get player information from the Slippi API'''
    query = '''
    query AccountManagementPageQuery($connect_code: String!) {
        getConnectCode(code: $connect_code) {
            user {
                displayName
                connectCode {
                    code
                }
                rankedNetplayProfile {
                    id
                    ratingOrdinal
                    ratingUpdateCount
                    wins
                    losses
                    dailyGlobalPlacement
                    dailyRegionalPlacement
                    continent
                    characters {
                        id
                        character
                        gameCount
                    }
                }
            }
        }
    }
    '''
    variables = { 'connect_code': connect_code };
    response = requests.post(BASE_URL, 
        json={
            'query': query, 
            'variables': variables
        }
    )
    return response.json()['data']


def connect_code_exists(connect_code):
    return not get_player_information(connect_code)['getConnectCode'] is None


