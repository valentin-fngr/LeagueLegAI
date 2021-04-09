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


async def write_in_csv(path,account_id, session):
    '''
        write matches inside the csv provided via path. 
        Arguments: 
            account_id : player account id
            session : async io session
    '''
    matches = await get_first_ten_matches(account_id, session)
    if not matches: 
        return matches 



async def get_first_ten_matches(account_id, session): 
    '''
        Return a list of 15 matches for a given user
    '''
    serialized_matches = []
    try: 
        print(f"Let's fetch matches for {account_id} ")
        match_history = await fetch_user_matches(account_id, session)  
        time.sleep(2.2)
        print("Succesfully fetched 2 matches")
        # get 15 matches
        for i in range(len(match_history)): 
            game_id = str(match_history[i]["gameId"]) 
            # fetch game details 
            print(f"Fetching match nb {i + 1} for account id : {account_id}")
            game_detail = await fetch_match_details(game_id, session) 
            print(f"Got game details ! for {game_id}")
            serialized_match = MatchSerializer.from_response_body(game_detail)
            serialized_matches.append(serialized_match)

        print(f"Returning {len(serialized_matches)} game for account id : {account_id}")
        return serialized_matches
    except Exception as e: 
        print(f"Couldn't fetch matches for user ID : {account_id}")
        print(f"Coudln't fetch for game id : {game_id}")
        print(e)



async def main(): 
    players_ids = set()
    for tier in TIER: 
        for division in DIVISION: 
            player_list = fetch_summoner_name_by_division(division, tier, queue=QUEUE) 
            
            print(f"Printing player list : {player_list}  \n")
            print(f"Received {len(player_list)} players \n")
            print(f"Fetching data for {len(player_list)} players \n")
            time.sleep(2)
            async with ClientSession() as session:
                tasks = []
                for player in player_list: 
                    # fetch user id 
                    account_id = await fetch_user_account_id(player, session)
                    print(account_id)
                    if account_id not in players_ids: 
                        players_ids.add(account_id) 
                        # fetch matches 
                        tasks.append(get_first_ten_matches(account_id, session))
                    else: 
                        print(f"Already porcessed {account_id}") 
                await asyncio.gather(*tasks)
        break 



if __name__ == "__main__": 
    asyncio.run(main())