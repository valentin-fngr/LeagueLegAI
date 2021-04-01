import pickle
from bs4 import BeautifulSoup
import requests
import os


GAMES_BY_RANK = 200
RANKS = ["I", "B", "S", "G", "P", "D", "M", "GM"]
LANES = ["haut", "jungle", "milieu", "bas", "support"]
CHAMPS = []

CHAMPS_URL = "https://euw.op.gg/champion/statistics"


def get_all_champs(): 
    '''
        return a list containing all champions and their main lanes
    '''
    champions_list = []
    # request 
    req = requests.get(CHAMPS_URL)
    content = req.text
    soup = BeautifulSoup(content, "html.parser")
    class_tag = "champion-index__champion-item"
    html_champs_list = soup.find_all(class_=class_tag)
    for item in html_champs_list: 
        champ_name = item["data-champion-name"]
        champions_list.append(champ_name) 

    print(f"Returned {len(champions_list)} champions ! \n")
    print(champions_list)
    # serializing champ list 
    try: 
        with open("champion_list.h5", "wb") as f: 
            pickle.dump({"champions_list" : champions_list}, f)
            print(" -- Champions list serialized -- ")
    except Exception as e: 
        print(e)
    
if __name__ == "__main__":
    get_all_champs()