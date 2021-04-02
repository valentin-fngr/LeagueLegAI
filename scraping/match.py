import requests
import os
import json
import datetime.datetime
# GET USER ID ! https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/oraxan{summonerName} | accountId
# GET MATCH BY USER : GET /lol/match/v4/matchlists/by-account/{encryptedAccountId}
# GET MATCH DETAILS : GET /lol/match/v4/matches/{matchId}
# GET CHAMP DETAILS : http://ddragon.leagueoflegends.com/cdn/11.7.1/data/en_US/champion/{champion}.json




#  ------------------------ | STRATEGY | --------------------------
    # GET USER ID (get suommer id )
    # GET MATCH (get match list)
    # GET DETAILS ( teams, items, champs_id, stats)
    # GET CHAMP (champ infos)
# -----------------------------------------------------------------
API_KEY = os.environ.get("RIOT_KEY")
USER_DETAIL_URL = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
MATCH_BY_USER_URL = "https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/"
MATCH_DETAILS_URL = "https://euw1.api.riotgames.com/lol/match/v4/matches/"
CHAMP_DETAIL_URL = "http://ddragon.leagueoflegends.com/cdn/11.7.1/data/en_US/champion/" # + champ.json

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
        print(content)

    except Exception as e: 
        raise e    
    finally: 
        return game_detail
        



class PlayerSerializer:

    def __init__(self, champion, rank): 
        self.champion = champion
        self.rank = rank

class TeamSerializer: 

    def __init__(self): 
        self.player1 = None # champ id and rank
        self.player2 = None 
        self.player3 = None 
        self.player4 = None 
        self.player5 = None 
        self.game_status = None # Win or Fail
        self.team_id = None
        self.firstBlood = None
        self.firstBlood = None 
        self.firstTower = None 
        self.firstBaron = None 
        self.firstDragon = None 
        self.towerKills = None
    
        

    @classmethod
    def from_dict(cls, team_response):
        team_data = {
            "teamId" : team_response["teamId"]
            "status" : team_response["win"], 
            "firstBlood" : team_response["firstBlood"],
            "firstTower" : team_response["firstTower"], 
            "firstBaron" : team_response["firstBaron"], 
            "firstDragon" : team_response["firstDragon"], 
            "towerKills" : team_response["towerKills"]
        }

        


class MatchSerializer: 
    
    def __init__(self, gameId, plateformId, gameDuration, seasonId, gameMode, teamOne, teamTwo, winner): 
        self.gameId = gameId 
        self.plateformId = plateformId 
        self.gameDuration = gameDuration
        self.seasonId = seasonId
        self.gameMode = gameMode
        # list of players in team 1
        self.teamOne = teamOne 
        # list of players in team 2 
        self.teamTwo = teamTwo
        self.winner = winner


    @classmethod 
    def from_response_body(cls, match_body): 
        '''
            return a MatchSerializer Instance with both team's informations set
            Arguments : 
                match_body : match_body from response
        '''
        match_gen_details = {
            "gameId" : match_body["gameId"], 
            "plateformeId" : match_body["plateformId"], 
            "gameDuration" : match_body["gameDuration"], 
            "seasonId" : match_body["seasonId"], 
            "gameMode" : match_body["gameMode"]
        }
        
        match_instance = cls(**match_gen_details)

        # build teams data 
        tea
        


    def to_csv(self, file_path): 
        # todo : format the instance as a csv
        pass


user_id = fetch_user_account_id("oraxan")
matches = fetch_user_matches(user_id)
match_id = str(matches[0]["gameId"])
print(match_id)
fetch_match_details(match_id)
