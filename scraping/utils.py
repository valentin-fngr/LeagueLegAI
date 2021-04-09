import os
import pickle
import asyncio
from aiohttp import ClientSession
import requests
import time
import json

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

LEAGUE_URL = "https://euw1.api.riotgames.com/lol/league/v4/entries"
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


async def fetch_user_matches(account_id, session, endIndex=2): 
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
        

def fetch_summoner_name_by_division(division, tier, queue): 
    '''
        return a list of summoner name of the first 10 pages by division
        Arguments: 
            divison : the division  1, 2, ...
            tier : The league name : Bronze, ... 
            queue : ranked solo or ranked 5v5
            
    '''
    players = set()
    for i in range(3): 
        page = i+1 
        url = LEAGUE_URL + f"/{queue}/{tier}/{division}?{page}"
        try: 
            r = requests.get(url, headers=headers)
            body = r.json()
            for player in body: 
                summonerName = player["summonerName"]
                if summonerName not in players: 
                    players.add(summonerName)
                    break
            break
        except Exception as e: 
            print(e)
            raise e
        time.sleep(3)

    return players


def get_champion_name(champion_id): 
    '''
        return a champion's name 
        Argument : champion id
    '''
    return CHAMPION_LIST[champion_id]
