print("do imports")

import aiohttp
import asyncio
import urllib.parse
from datetime import datetime
from io import StringIO

print("constants")

with open("api.key") as f:
    api_key = f.read().strip()

print("set functions")

async def get_puuid(session, name):
    name = urllib.parse.quote_plus(name)
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}"
    async with session.get(url) as resp:
        details = await resp.json()
        print(details)
        return details["puuid"]

async def get_game_details(session, match):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match}?api_key={api_key}"
    async with session.get(url) as resp:
        details = await resp.json()
        return details

async def get_games(session, puuid):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={api_key}"
    async with session.get(url) as resp:
        games = await resp.json()
        print(games)
        return games

async def get_game_details_for_games(session, puuid):
    games = await get_games(session, puuid)
    game_details_tasks = map(lambda g: get_game_details(session, g),games)
    return await asyncio.gather(*game_details_tasks)

async def get_sum_last_games_filtered(session,puuid):
    data = await get_game_details_for_games(session,puuid)
    def extract_player_data(p):
        return p["summonerName"],p["totalDamageDealt"],p["championName"],p["win"]
    def extract_game_data(g):
        return g["gameStartTimestamp"],map(extract_player_data, g["participants"])
    filtered_data = data
    filtered_data = filter(lambda g: "info" in g,filtered_data)
    filtered_data = map(lambda g: g["info"],filtered_data)
    filtered_data = map(extract_game_data,filtered_data)
    return list(map(lambda g: (g[0],list(g[1])),filtered_data))

def eval_sum_game(summoner_name,g):
    best_player = max(g[1],key=lambda p: p[1])
    agurin = next(iter(filter(lambda p: p[0] == summoner_name,g[1])))
    return best_player[0] == summoner_name, agurin[2], agurin[3], g[0]

async def load_data_async(summoner_name):
    ret_string = StringIO()

    def add_row(rstr,geval,champ,str_time):
        rstr.write(f"<tr><td>{geval}</td><td>{champ}</td><td>{str_time}</td></tr>")

    #add_row(ret_string,"test","test","test")
        
    async with aiohttp.ClientSession() as session:
        puuid = await get_puuid(session,summoner_name)
        data = await get_sum_last_games_filtered(session,puuid)
        for mostdmg, champ, win, time in map(lambda d: eval_sum_game(summoner_name,d),data):
            str_time = datetime.utcfromtimestamp(time/1000).strftime('%Y-%m-%d %H:%M:%S')
            if mostdmg and win:
                add_row(ret_string,"gecarried",champ,str_time)
            elif not mostdmg and not win:
                add_row(ret_string,"geinted",champ,str_time)
            else:
                add_row(ret_string,"ok",champ,str_time)
    
    return ret_string.getvalue()

def load_data(summoner_name):
    print("load data")
    return asyncio.run(load_data_async(summoner_name))

def lambda_handler(event, context):

    summoner_name = "Agurin"
    
    if event is not None:
        if "queryStringParameters" in event:
            if event["queryStringParameters"] is not None:
                if "summonerName" in event["queryStringParameters"]:
                    summoner_name = event["queryStringParameters"]["summonerName"]        

    data = load_data(summoner_name)

    with open("template_website.html") as f:
        html_template = f.read()
    body = html_template.replace("pythondata",data)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=UTF-8"
        },
        "body": body
    }
    
    
print("functions loaded")

if __name__ == "__main__":
    print(lambda_handler(None,None))