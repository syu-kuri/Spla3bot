import datetime
import requests

def user_agent():
    headers = {
        'User-Agent': "Spla3 Discord Bot (Twitter： @syukur1ch、Discord： シュークリーム#9118)".encode()
    }
    return headers

def get_schedule(p1, p2):
    url = "https://spla3.yuu26.com/api/"
    res = requests.get(f"{url}{p1}/{p2}", headers=user_agent())
    if res.status_code == 200:
        data = res.json()
        results = data['results'][0]
        return results

def get_all_schedule(p1):
    url = "https://spla3.yuu26.com/api/"
    res = requests.get(f"{url}{p1}/schedule", headers=user_agent())
    if res.status_code == 200:
        data = res.json()
        results = data['results']
        return results

def time_molding(p1):
    _time = datetime.datetime.strptime(p1, '%Y-%m-%dT%H:%M:%S%z')
    time = _time.strftime('%m/%d %H:%M')
    return time

def molding(p1):
    data = p1
    st = data["start_time"]
    et = data["end_time"]
    rule_name = data["rule"]["name"]
    stages = []
    for stage in data["stages"]:
        stages.append(stage["name"])

    start_time = time_molding(st)
    end_time = time_molding(et)

    return [start_time, end_time, rule_name, stages]

def coop_molding(p1):
    data = p1
    st = data["start_time"]
    et = data["end_time"]
    stage = data["stage"]["name"]

    start_time = time_molding(st)
    end_time = time_molding(et)

    weapons = []
    for weapon in data["weapons"]:
        weapons.append(weapon["name"])

    return[start_time, end_time, stage, weapons]

def schedule_molding(p1):
    all_data = get_all_schedule(p1)
    results = []
    for num in range(len(all_data)):
        results.append(molding(all_data[num]))
    return results

def coop_schedule_molding(p1):
    all_data = get_all_schedule(p1)
    results = []
    for num in range(len(all_data)):
        results.append(coop_molding(all_data[num]))
    return results

def get_rule_image(p1):
    rule_images = {
        "ナワバリバトル": "https://images-ext-1.discordapp.net/external/sNH8hPsRSuUYU7eMhUebaL7v8I3q82OepAd-vN_5sWE/https/www.nintendo.co.jp/switch/aab6a/assets/images/battle-sec01_logo.png",
        "バンカラマッチ": "https://media.discordapp.net/attachments/808221718106603540/812571951872081920/battle-sec02_logo.png",
        "サーモンラン": "https://cdn.discordapp.com/attachments/808221718106603540/1021002540193685554/unknown.png",
        "ガチエリア": "https://cdn.discordapp.com/attachments/808221718106603540/815038217400090634/show.png",
        "ガチヤグラ": "https://cdn.discordapp.com/attachments/808221718106603540/815038610101370980/show.png",
        "ガチホコバトル": "https://cdn.discordapp.com/attachments/808221718106603540/815040449055162368/show.png",
        "ガチアサリ": "https://cdn.discordapp.com/attachments/808221718106603540/815040479166595092/show.png"
    }
    return rule_images.get(p1)

def get_coop_image(p1):
    stage_images = {
        "アラマキ砦": "https://cdn.discordapp.com/attachments/808221718106603540/1020996240466526218/unknown.png",
        "ムニ・エール海洋発電所": "https://cdn.discordapp.com/attachments/808221718106603540/1020999594936635402/unknown.png",
        "シェケナダム": "https://cdn.discordapp.com/attachments/808221718106603540/1020997322685022238/unknown.png"
    }
    return stage_images.get(p1)