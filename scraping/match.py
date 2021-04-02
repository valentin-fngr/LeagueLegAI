import requests
import os
import json
import datetime
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
        


# DONE 
class PlayerSerializer:

    def __init__(self): 
        self.championId = None
        self.championName = None
        self.kills = None 
        self.deaths = None 
        self.assists = None 
        self.totalDamageDealt = None 
        self.visionScore = None
        self.totalDamageTaken = None
        self.turretKills = None
        self.totalMinionsKilled = None
        self.champLevel = None
        self.wardsKilled = None
        

    @classmethod 
    def from_ParticipantStatsDto(self, ParticipantStatsDto): 
        # print(ParticipantStatsDto)
        player_serializer = PlayerSerializer() 
        data = {}
        for attr in player_serializer.__dict__.keys(): 
            print(attr)
            if attr in ParticipantStatsDto:
                data[attr] = ParticipantStatsDto[attr]
            elif attr in ParticipantStatsDto["status"]: 
                data[attr] = ParticipantStatsDto["status"][attr]
            else: 
                raise Exception(f"Error : cannot retrieve attribute {attr} from the ParticipantStatsDto body.")
        
        return player_serializer(**data)

    def to_dict(self): 
        return self.__dict__


# DONE
class TeamSerializer: 

    def __init__(self): 
        self.player1 = None # champ 
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
    def from_dict(cls, TeamStatsDto, participantList):
        '''
            return a TeamSerializer instance 
            Arguments : 
                TeamStateDto : A single TeamStatsDto object, 1 team only, 
                participantList : A list of all players in a team
        '''
        print(participantList)
        data = {
            "teamId" : TeamStatsDto["teamId"],
            "status" : TeamStatsDto["win"], 
            "firstBlood" : TeamStatsDto["firstBlood"],
            "firstTower" : TeamStatsDto["firstTower"], 
            "firstBaron" : TeamStatsDto["firstBaron"], 
            "firstDragon" : TeamStatsDto["firstDragon"], 
            "towerKills" : TeamStatsDto["towerKills"]
        }

        for idx, player in enumerate(participantList): 
            player_obj = PlayerSerializer.from_ParticipantStatsDto(player)
            data["player"+idx] = to_dict.to_dict()

        serialized_team = TeamSerializer(**team_data) 
        return serialized_team

    def to_dict(self): 
        return self.__dict__


class MatchSerializer: 
    
    def __init__(self): 
        self.gameId = None 
        self.platformId = None 
        self.gameDuration = None
        self.seasonId = None
        self.gameMode = None
        # list of players in team 1
        self.teamOne = None 
        # list of players in team 2 
        self.teamTwo = None
        self.winner = None


    @classmethod 
    def from_response_body(cls, match_body): 
        '''
            return a MatchSerializer Instance with both team's informations set
            Arguments : 
                match_body : match_body from response
        '''
        match_gen_details = {
            "gameId" : match_body["gameId"], 
            "platformId" : match_body["platformId"], 
            "gameDuration" : match_body["gameDuration"], 
            "seasonId" : match_body["seasonId"], 
            "gameMode" : match_body["gameMode"]
        }

        match_obj = cls(**match_gen_details)

        for i in range(0, 2): 
            # get gen team data 
            team_meta = match_body["team"]
            team_id = team_meta["teamId"]
            # get players from team 
            players_list = [player for player in match_body["participants"] if player["teamId"] == team_id]
            print(f"Player list size : {len(players_list)} \n")
            #serializing 
            team_serializer = TeamSerializer.from_dict()     
            team_obj = team_serializer.to_dict()
            if i == 0: 
                match_obj.teamOne = team_obj
            else: 
                match_obj.teamTwo = team_obj
        
        return match_obj

    def to_csv(self, file_path): 
        # todo : format the instance as a csv
        pass


user_id = fetch_user_account_id("oraxan")
print(user_id)
matches = fetch_user_matches(user_id)
match_id = str(matches[0]["gameId"])
match_resp = fetch_match_details(match_id)


match_object = MatchSerializer.from_response_body(match_resp)