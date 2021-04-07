import asyncio
from aiohttp import ClientSession
from utils import (fetch_match_details, fetch_user_account_id, fetch_user_matches, get_champion_name)
from serializer import * 

#  ------------------------ | STRATEGY | --------------------------
    # GET USER ID (get suommer id )
    # GET MATCH (get match list)
    # GET DETAILS ( teams, items, champs_id, stats)
    # GET CHAMP (champ infos)
# -----------------------------------------------------------------

async def serialize_match(game_id, session): 
    '''
        return a serialized match (json) from a summoner's name 
        Arguments: 
            match_detail : a match's id 
            sessiosn : aiothttp session
    '''
    match_body = await fetch_match_details(game_id, session)  
    serialized_match = MatchSerializer.from_response_body(match_body).to_dict()
    print(json.dumps(serialized_match, indent=4))
    return serialized_match


async def get_matches(summoner_name):
    '''
        return a serialized match (json) from a summoner's name 
        Arguments: 
            summoner_name : a summoner's name, 
    ''' 
    async with ClientSession() as session: 
        try: 
            account_id = await fetch_user_account_id(summoner_name, session)
            print(account_id)
            matches = await fetch_user_matches(account_id, session)
        #TO DO  : REMOVE EXCEPTIONS FROM THE UTILITY FUNCTIONS ! 
        except Exception as e:
            print(e)
            print("Something went wrong getting the account")
            return None

        tasks = []
        
        for idx, match in enumerate(matches): 
            game_id = str(match["gameId"])
            tasks.append(serialize_match(game_id, session))
            print("done with " + str(idx+1))

        await asyncio.gather(*tasks)

        
if __name__ == "__main__": 
    # TO DO : add a functin for it 
    asyncio.run(get_matches("oraxan"))