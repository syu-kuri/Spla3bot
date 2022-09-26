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