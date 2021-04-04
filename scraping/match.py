import os
import requests
import json
import datetime
import pickle
from utils import (fetch_match_details, fetch_user_account_id, fetch_user_matches, get_champion_name)




class PlayerSerializer:

    def __init__(self, *args, **kwargs): 
        self.championId = str(kwargs.get("championId", None))
        self.championName = kwargs.get("championName", None)
        self.kills = kwargs.get("kills", None) 
        self.deaths = kwargs.get("deaths", None) 
        self.assists = kwargs.get("assists", None) 
        self.totalDamageDealt = kwargs.get("totalDamageDealt", None) 
        self.visionScore = kwargs.get("visionScore", None)
        self.totalDamageTaken = kwargs.get("totalDamageTaken", None)
        self.turretKills = kwargs.get("turretKills", None)
        self.totalMinionsKilled = kwargs.get("totalMinionsKilled", None)
        self.champLevel = kwargs.get("champLevel", None)
        self.wardsKilled = kwargs.get("wardsKilled", None)

    @classmethod 
    def from_ParticipantStatsDto(cls, ParticipantStatsDto): 
        data = {}
        attributes = list(cls().__dict__.keys())
        # we will handle championName after everything
        attributes.remove("championName")
        for attr in attributes: 
            if attr in ParticipantStatsDto:
                data[attr] = ParticipantStatsDto[attr]
            elif attr in ParticipantStatsDto["stats"]: 
                data[attr] = ParticipantStatsDto["stats"][attr]
            else: 
                # handle errors
                print(f"Error : cannot retrieve attribute {attr} from the ParticipantStatsDto body.")

        # get champion's name
        player_instance = cls(**data)
        champ_id = player_instance.championId
        player_instance.championName = get_champion_name(champ_id)

        return player_instance

    def to_dict(self): 
        return self.__dict__


# DONE
class TeamSerializer: 

    def __init__(self, *args, **kwargs): 
        self.player1 = kwargs.get("player1", None) # champ 
        self.player2 = kwargs.get("player2", None) 
        self.player3 = kwargs.get("player3", None) 
        self.player4 = kwargs.get("player4", None) 
        self.player5 = kwargs.get("player5", None) 
        self.status = kwargs.get("status", None) # Win or Fail
        self.teamId = kwargs.get("teamId", None)
        self.firstBlood = kwargs.get("firstBlood", None)
        self.firstBlood = kwargs.get("firstBlood", None) 
        self.firstTower = kwargs.get("firstTower", None) 
        self.firstBaron = kwargs.get("firstBaron", None) 
        self.firstDragon = kwargs.get("firstDragon", None) 
        self.towerKills = kwargs.get("towerKills", None)
    
        
    @classmethod
    def from_dict(cls, TeamStatsDto, participantList):
        '''
            return a TeamSerializer instance 
            Arguments : 
                TeamStateDto : A single TeamStatsDto object, 1 team only, 
                participantList : A list of all players in a team
        '''
        print("Printin team's players ! ")
        # print(participantList)
        data = {
            "teamId" : TeamStatsDto["teamId"],
            "status" : TeamStatsDto["win"], 
            "firstBlood" : TeamStatsDto["firstBlood"],
            "firstTower" : TeamStatsDto["firstTower"], 
            "firstBaron" : TeamStatsDto["firstBaron"], 
            "firstDragon" : TeamStatsDto["firstDragon"], 
            "towerKills" : TeamStatsDto["towerKills"]
        }
        print(data)

        for idx, player in enumerate(participantList): 
            print(idx)
            player_obj = PlayerSerializer.from_ParticipantStatsDto(player)
            data["player"+str(idx + 1)] = player_obj.to_dict()

        serialized_team = TeamSerializer(**data) 
        return serialized_team

    def to_dict(self): 
        return self.__dict__


class MatchSerializer: 
    
    def __init__(self, *args, **kwargs): 
        self.gameId = kwargs.get("gameId", None) 
        self.platformId = kwargs.get("platformId", None) 
        self.gameDuration = kwargs.get("gameDuration", None)
        self.seasonId = kwargs.get("seasonId", None)
        self.gameMode = kwargs.get("gameMode", None)
        # list of players in team 1
        self.teamOne = kwargs.get("teamOne", None) 
        # list of players in team 2 
        self.teamTwo = kwargs.get("teamTwo", None)


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
            team_meta = match_body["teams"][i]
            team_id = team_meta["teamId"]
            # get players from team 
            players_list = [player for player in match_body["participants"] if player["teamId"] == team_id]
            print(f"Player list size : {len(players_list)} \n")
            #serializing 
            team_serializer = TeamSerializer.from_dict(team_meta, players_list)     
            team_obj = team_serializer.to_dict()
            if i == 0: 
                match_obj.teamOne = team_obj
            else: 
                match_obj.teamTwo = team_obj
        
        return match_obj

    def __repr__(self): 
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self): 
        return self.__dict__

    def to_csv(self, file_path): 
        # todo : format the instance as a csv
        pass


# test 

# user_id = fetch_user_account_id("oraxan")
# matches = fetch_user_matches(user_id)
# match_id = str(matches[3]["gameId"])
# match_resp = fetch_match_details(match_id)


# match_object = MatchSerializer.from_response_body(match_resp)
# print(match_object)