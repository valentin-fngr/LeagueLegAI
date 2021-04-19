import pickle
import requests 
import os

URL = "http://ddragon.leagueoflegends.com/cdn/11.8.1/data/en_US/champion.json"
API_KEY = os.environ.get("RIOT_KEY")
headers = {
    "X-Riot-Token": API_KEY
}


def main(): 
    champion_dict = {}
    
    try: 
        r = requests.get(URL, headers=headers)
        content = r.json()
        data = content["data"]
        for champion in data:   
            champion_dict[data[champion]["key"]] = data[champion]["name"]

        # serialize the list 
        with open("champion_list", "wb") as f: 
            pickle.dump({"champion_list" : champion_dict}, f)
            print("Successfully serialized the champion_list ! ")
            print(f"Total champs : {len(champion_dict)}")
        
        print(champion_dict)
    except Exception as e: 
        raise e
        
        

if __name__ == "__main__":
    main()
