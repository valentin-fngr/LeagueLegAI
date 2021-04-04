import os
import requests
import pickle
# GET USER ID ! https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/oraxan{summonerName} | accountId
# GET MATCH BY USER : GET /lol/match/v4/matchlists/by-account/{encryptedAccountId}
# GET MATCH DETAILS : GET /lol/match/v4/matches/{matchId}
# GET CHAMP DETAILS : http://ddragon.leagueoflegends.com/cdn/11.7.1/data/en_US/champion.json

#  ------------------------ | STRATEGY | --------------------------
    # GET USER ID (get suommer id )
    # GET MATCH (get match list)
    # GET DETAILS ( teams, items, champs_id, stats)
    # GET CHAMP (champ infos)
# -----------------------------------------------------------------
with open("champion_list", "rb") as f: 
    CHAMPION_LIST = pickle.load(f)["champion_list"]
API_KEY = os.environ.get("RIOT_KEY")
USER_DETAIL_URL = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
MATCH_BY_USER_URL = "https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/"
MATCH_DETAILS_URL = "https://euw1.api.riotgames.com/lol/match/v4/matches/"
CHAMPIONS_URL = "http://ddragon.leagueoflegends.com/cdn/11.7.1/data/en_US/champion.json"
headers = {
    "X-Riot-Token": API_KEY
}

def fetch_user_account_id(summoner_name): 
    '''
        fetch a user account's details
    '''
    url = USER_DETAIL_URL + summoner_name 
    accountId = None
    try: 
        r = requests.get(url, headers=headers)
        content = r.json()
        # get account id
        accountId = content["accountId"] 

    except Exception as e: 
        raise e
    finally: 
        return accountId        


def fetch_user_matches(account_id, endIndex=30): 
    '''
        fetch user's latest 30 matches
    '''
    print(account_id)
    url = MATCH_BY_USER_URL + account_id
    matches = []
    params = {"endIndex" : endIndex}
    try: 
        r = requests.get(url, headers=headers, params=params) 
        content = r.json() 
        matches = content["matches"]
        print(f"Retrieved {len(matches)} matches for {account_id}")
    except Exception as e: 
        raise e
    finally: 
        return matches


def fetch_match_details(match_id): 
    '''
        return a single match details response's body
    '''
    url = MATCH_DETAILS_URL + match_id
    game_detail = {}
    try: 
        r = requests.get(url, headers=headers)
        game_detail = r.json()

    except Exception as e: 
        raise e    
    finally: 
        return game_detail
        

def get_champion_name(champion_id): 
    '''
        return a champion's name 
        Argument : champion id
    '''
    return CHAMPION_LIST[champion_id]
