import asyncio
from aiohttp import ClientSession
from utils import (fetch_match_details, fetch_user_account_id, fetch_user_matches, get_champion_name, fetch_summoner_name_by_division)
from serializer import * 
import time
#  ------------------------ | STRATEGY | --------------------------
    # GET USER ID (get suommer id )
    # GET MATCH (get match list)
    # GET DETAILS ( teams, items, champs_id, stats)
    # GET CHAMP (champ infos)
# -----------------------------------------------------------------

DIVISION = ["I", "II", "III", "IV"]
TIER = ["IRON", "SILVER", "BRONZE", "GOLD", "PLATINIUM", "DIAMOND"]
QUEUE = "RANKED_SOLO_5x5"


async def get_first_ten_matches(account_id, session): 
    '''
        Return a list of 15 matches for a given user
    '''
    serialized_matches = []
    try: 
        match_history = await fetch_user_matches(account_id, session)  
        # get 15 matches
        for i in range(15): 
            game_id = str(match_history[i]["gameId"]) 
            # fetch game details 
            game_detail = await fetch_match_details(game_id, session) 
            serialized_match = MatchSerializer.from_response_body(game_detail)
            serialized_matches.append(serialized_match)
            return serialized_matches
    except Exception as e: 
        print(f"Couldn't fetch matches for user ID : {account_id}")
        print(e) 



async def main(): 
    players_ids = set()
    for tier in TIER: 
        for division in DIVISION: 
            player_list = fetch_summoner_name_by_division(division, tier, queue=QUEUE) 
            print(player_list)
            print(f"Received {len(player_list)} players \n")
            print(f"Fetching data for {len(player_list)} players")
            time.sleep(2)
            async with ClientSession() as session:
                tasks = []
                for player in player_list: 
                    # fetch user id 
                    account_id = await fetch_user_account_id(player, session)
                    if account_id not in players_ids: 
                        players_ids.add(account_id) 
                        # fetch matches 
                        tasks.append(get_first_ten_matches(account_id, session))
                        print("Added one game ")
                    else: 
                        print(f"Already processed {account_id}") 
                await asyncio.gather(*tasks)
        break 



if __name__ == "__main__": 
    asyncio.run(main())