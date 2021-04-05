import os
import pickle
import asyncio
from aiohttp import ClientSession
import requests


"""
    Utility functions to fetch informations from the riot API

"""

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


async def fetch_user_account_id(summoner_name, session): 
    '''
        fetch a user account's details
        Argument : 
            summoner_name(str), 
            session : aiohttp session
    '''
    url = USER_DETAIL_URL + summoner_name 
    accountId = None
    try: 
        r = await session.request(method="GET", url=url, headers=headers)
        r.raise_for_status()
        content = await r.json()
        # get account id
        accountId = content["accountId"] 

    except Exception as e: 
        print(e)
        raise e
    finally: 
        return accountId        


async def fetch_user_matches(account_id, session, endIndex=10): 
    '''
        fetch user's latest 30 matches
        Argument: 
            account_id : encrypted account_id
            session : session, 
            endIndex : maximum number of matches to fetch
    '''
    url = MATCH_BY_USER_URL + account_id
    matches = []
    params = {"endIndex" : endIndex}
    try: 
        r = await session.request(method="GET", url=url, headers=headers, params=params) 
        r.raise_for_status()
        content = await r.json()
        matches = [match for match in content["matches"] if match is not None]
        print(f"Retrieved {len(matches)} matches for {account_id}")
    except Exception as e: 
        raise e
    finally: 
        return matches


async def fetch_match_details(match_id, session): 
    '''
        return a single match details response's body
        Argument: 
            match_id : a match's id
            session : session
    '''
    url = MATCH_DETAILS_URL + match_id
    game_detail = {}
    try: 
        r = await session.request(method="GET", url=url, headers=headers)
        r.raise_for_status()
        game_detail = await r.json()

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
