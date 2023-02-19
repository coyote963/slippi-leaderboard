def generic_api_response(
    rating=1000,
    wins=1,
    losses=1,
    characters=[],
    displayName='example'
    ):
    return {
        "getConnectCode":{
            "user":{
                "displayName":displayName,
                "rankedNetplayProfile":{
                    "ratingOrdinal":rating,
                    "wins":wins,
                    "losses":losses,
                    "characters": characters
                }
            }
        }
    }