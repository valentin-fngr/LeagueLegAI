import os 
import csv 
import asyncio
from aiohttp import ClientSession
import time
import aiofiles
from utils import (fetch_match_details, fetch_user_account_id, fetch_user_matches, get_champion_name, fetch_summoner_name_by_division)
from serializer import * 
import aiohttp

#  ------------------------ | STRATEGY | --------------------------
    # GET USER ID (get suommer id )
    # GET MATCH (get match list)
    # GET DETAILS ( teams, items, champs_id, stats)
    # GET CHAMP (champ infos)
# -----------------------------------------------------------------

DIVISION = ["I", "II", "III", "IV"]
TIER = ["IRON", "SILVER", "BRONZE", "GOLD", "PLATINIUM", "DIAMOND"]
QUEUE = "RANKED_SOLO_5x5"
CSV_PATH = os.path.join(os.getcwd(), "dataset2.csv")

INITIAL_ROW = [
    "gameId", "plateformId", "gameDuration", "seasonId", "gameMode", 
    "participantId_x1", "matchHistoryUri_x1", "championId_x1", "championName_x1", "kills_x1", "deaths_x1", "assists_x1", "totalDammageDealt_x1", "visionScore_x1", "totalDamageTaken_x1", "turretKills_x1", "totalMinionsKilled_x1","champLevel_x1", 
    "participantId_x2", "matchHistoryUri_x2", "championId_x2", "championName_x2", "kills_x2", "deaths_x2", "assists_x2", "totalDammageDealt_x2", "visionScore_x2", "totalDamageTaken_x2", "turretKills_x2", "totalMinionsKilled_x2","champLevel_x2", 
    "participantId_x3", "matchHistoryUri_x3", "championId_x3", "championName_x3", "kills_x3", "deaths_x3", "assists_x3", "totalDammageDealt_x3", "visionScore_x3", "totalDamageTaken_x3", "turretKills_x3", "totalMinionsKilled_x3","champLevel_x3", 
    "participantId_x4", "matchHistoryUri_x4", "championId_x4", "championName_x4", "kills_x4", "deaths_x4", "assists_x4", "totalDammageDealt_x4", "visionScore_x4", "totalDamageTaken_x4", "turretKills_x4", "totalMinionsKilled_x4","champLevel_x4", 
    "participantId_x5", "matchHistoryUri_x5", "championId_x5", "championName_x5", "kills_x5", "deaths_x5", "assists_x5", "totalDammageDealt_x5", "visionScore_x5", "totalDamageTaken_x5", "turretKills_x5", "totalMinionsKilled_x5","champLevel_x5", 
    "is_winner_x", "teamId_x", "firstBlood_x", "firstTower_x", "firstBaron_x", "firstDragon_x",
    "participantId_y1", "matchHistoryUri_y1", "championId_y1", "championName_y1", "kills_y1", "deaths_y1", "assists_y1", "totalDammageDealt_y1", "visionScore_y1", "totalDamageTaken_y1", "turretKills_y1", "totalMinionsKilled_y1","champLevel_y1", 
    "participantId_y2", "matchHistoryUri_y2", "championId_y2", "championName_y2", "kills_y2", "deaths_y2", "assists_y2", "totalDammageDealt_y2", "visionScore_y2", "totalDamageTaken_y2", "turretKills_y2", "totalMinionsKilled_y2","champLevel_y2", 
    "participantId_y3", "matchHistoryUri_y3", "championId_y3", "championName_y3", "kills_y3", "deaths_y3", "assists_y3", "totalDammageDealt_y3", "visionScore_y3", "totalDamageTaken_y3", "turretKills_y3", "totalMinionsKilled_y3","champLevel_y3", 
    "participantId_y4", "matchHistoryUri_y4", "championId_y4", "championName_y4", "kills_y4", "deaths_y4", "assists_y4", "totalDammageDealt_y4", "visionScore_y4", "totalDamageTaken_y4", "turretKills_y4", "totalMinionsKilled_y4","champLevel_y4", 
    "participantId_y5", "matchHistoryUri_y5", "championId_y5", "championName_y5", "kills_y5", "deaths_y5", "assists_y5", "totalDammageDealt_y5", "visionScore_y5", "totalDamageTaken_y5", "turretKills_y5", "totalMinionsKilled_y5","champLevel_y5", 
    "is_winner_y", "teamId_y", "firstBlood_y", "firstTower_y", "firstBaron_y", "firstDragon_y"
]

async def write_in_csv(summonerName, session, limit, path=CSV_PATH):
    
    '''
        write matches inside the csv provided via path. 
        Arguments: 
            account_id : player account id
            session : async io session
    '''
    matches = await get_first_ten_matches(summonerName, session, limit)
    if not matches: 
        return matches 
    else: 
        async with aiofiles.open(path, "a", newline='') as csvfile: # create the file if doesn't exist
            writer = csv.writer(csvfile) # csv writer
            print(f"writing for {len(matches)} matches !")
            for match in matches: 
                print(match)
                match_id = str(match.to_dict()["gameId"]) 
                # fill csv's rows
                await writer.writerow(match.as_row())
    

async def get_first_ten_matches(summonerName, session,limit): 
    '''
        Return a list of 15 matches for a given user
    '''
    async with limit: 
        serialized_matches = []
        try: 
            account_id = await fetch_user_account_id(summonerName, session)
            await asyncio.sleep(1)
            print(f"Trying to fetch match_history")
            match_history = await fetch_user_matches(account_id, session)
            await asyncio.sleep(1)
            print(f"Succesfully fetched {len(match_history)} matches for account id : {account_id}\n")

        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError) as e:
            print("IO Exception -----------") 
            print("Failed fetching match history")
            print(e, "\n")
        except Exception as e: 
            print("Non io Exception occured ---------")
            print(f"Coudln't fetch matches for account_id  : {summonerName}")
        else: 
            # iterating over matches
            for i in range(len(match_history)): 
                game_id = str(match_history[i]["gameId"]) 
                # fetch game details 
                print(f"Fetching match nb {i + 1} for account id : {account_id}")
                try: 
                    game_detail = await fetch_match_details(game_id, session) 
                    await asyncio.sleep(1)
                except Exception as e: 
                    print("Non io Exception occured ---------")
                    print(f"Coudln't fetch for game id : {game_id}")
                    print(f"Following Exception occured {e} \n")
                else: 
                    print(f"Successfully fetched : {game_detail['gameId']} plateformId : {game_detail['platformId']} \n")
                    serialized_match = MatchSerializer.from_response_body(game_detail)
                    print(serialized_match)
                    # adding the MatchSerializer instance here, not a dict ! 
                    serialized_matches.append(serialized_match)
            
        #returning matches
        return serialized_matches


async def main(): 
    print(len(INITIAL_ROW))
    with open(CSV_PATH, "w", newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(INITIAL_ROW)

    for tier in TIER: 
        for division in DIVISION: 
            player_list = fetch_summoner_name_by_division(division, tier, queue=QUEUE) 
            await asyncio.sleep(1)
            print(f"Received {len(player_list)} players \n")
            limit = asyncio.Semaphore(2)
            async with ClientSession() as session:
                tasks = []
                for summonerName in player_list: 
                    tasks.append(write_in_csv(summonerName, session, limit))
                await asyncio.gather(*tasks)
        print(f"Done with {tier} | {division}")

if __name__ == "__main__": 
    asyncio.run(main())