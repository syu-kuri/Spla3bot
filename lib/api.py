import requests

def user_agent():
    headers = {
        'User-Agent': "Spla3 Discord Bot (Twitter： @syukur1ch、Discord： シュークリーム#9118)".encode()
    }
    return headers

def get_schedule(rule, time_slot):
    url = "https://spla3.yuu26.com/api/"
    res = requests.get(f"{url}{rule}/{time_slot}", headers=user_agent())
    if res.status_code == 200:
        data = res.json()
        results = data['results'][0]
        return results

def get_all_schedule(rule):
    url = "https://spla3.yuu26.com/api/"
    res = requests.get(f"{url}{rule}/schedule", headers=user_agent())
    if res.status_code == 200:
        data = res.json()
        results = data['results']
        return results