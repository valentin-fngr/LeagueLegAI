import os 
import csv 
import asyncio
from aiohttp import ClientSession
import time
import aiofiles
from utils import (fetch_match_details, fetch_user_account_id, fetch_user_matches, get_champion_name, fetch_summoner_name_by_division)
from serializer import * 

#  ------------------------ | STRATEGY | --------------------------
    # GET USER ID (get suommer id )
    # GET MATCH (get match list)
    # GET DETAILS ( teams, items, champs_id, stats)
    # GET CHAMP (champ infos)
# -----------------------------------------------------------------

DIVISION = ["I", "II", "III", "IV"]
TIER = ["IRON", "SILVER", "BRONZE", "GOLD", "PLATINIUM", "DIAMOND"]
QUEUE = "RANKED_SOLO_5x5"
CSV_PATH = os.path.join(os.getcwd(), "dataset.csv")


async def write_in_csv(account_id, session, path=CSV_PATH):
    '''
        write matches inside the csv provided via path. 
        Arguments: 
            account_id : player account id
            session : async io session
    '''
    matches = await get_first_ten_matches(account_id, session)
    if not matches: 
        return matches 
    # if not os.path.exists(path): 
    #     raise ValueError(f"Provided path : {path} doesn't exist")
    else: 
        async with aiofiles.open(path, "w", newline='') as csvfile: # create the file if doesn't exist
            writer = csv.writer(csvfile) # csv writer

            print(f"writing for {len(matches)} matches !")
            for match in matches: 
                match_id = str(match.to_dict()["gameId"]) 
                # fill csv's rows
                await writer.writerow(match.as_row())
        

async def get_first_ten_matches(account_id, session): 
    '''
        Return a list of 15 matches for a given user
    '''
    serialized_matches = []
    try: 
        print(f"Let's fetch matches for {account_id} \n")
        match_history = await fetch_user_matches(account_id, session)  
        time.sleep(2.2)
        print(f"Succesfully fetched {len(match_history)} matches for account id : {account_id}\n")

    except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError) as e:
        print("IO Exception -----------") 
        print(e, "\n")
    except Exception as e: 
        print("Non io Exception occured ---------")
        print(f"Coudln't fetch matches for account_id  : {account_id}")
    else: 
        for i in range(len(match_history)): 
            game_id = str(match_history[i]["gameId"]) 
            # fetch game details 
            print(f"Fetching match nb {i + 1} for account id : {account_id}")
            try: 
                 game_detail = await fetch_match_details(game_id, session) 
                #  break # ------------ REMOVE --------------------- #
            except Exception as e: 
                print("Non io Exception occured ---------")
                print(f"Coudln't fetch for game id : {game_id}")
                print(f"Following Exception occured {e} \n")
            else: 
                print(f"Successfully fetched : {game_detail['gameId']} plateformId : {game_detail['platformId']} \n")
                serialized_match = MatchSerializer.from_response_body(game_detail)
                # adding the MatchSerializer instance here, not a dict ! 
                serialized_matches.append(serialized_match)
                time.sleep(2)   
        
    #returning matches
    return serialized_matches


async def main(): 
    players_ids = set()
    for tier in TIER: 
        for division in DIVISION: 
            print(f"Fetching players from : {tier}-{division}\n")
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
                    if account_id not in players_ids: 
                        players_ids.add(account_id) 
                        # fetch matches 
                        tasks.append(write_in_csv(account_id, session))
                    else: 
                        print(f"Already porcessed {account_id}") 
                await asyncio.gather(*tasks)
                break
        break 



if __name__ == "__main__": 
    asyncio.run(main())