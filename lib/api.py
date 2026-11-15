import asyncio

import aiohttp


API_BASE_URL = "https://spla3.yuu26.com/api/"
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=10)


class Spla3APIError(RuntimeError):
    pass


def user_agent():
    return {
        "User-Agent": "Spla3 Discord Bot (Twitter: @syukur1ch; Discord: syukur1ch)"
    }


async def _get_json(path: str):
    url = f"{API_BASE_URL}{path}"
    try:
        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT, headers=user_agent()) as session:
            async with session.get(url) as res:
                if res.status != 200:
                    raise Spla3APIError(f"Spla3 API returned HTTP {res.status}")
                return await res.json()
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        raise Spla3APIError("Failed to request Spla3 API") from e


async def get_schedule(rule, time_slot):
    data = await _get_json(f"{rule}/{time_slot}")
    try:
        return data["results"][0]
    except (KeyError, IndexError) as e:
        raise Spla3APIError("Spla3 API response did not include schedule results") from e


async def get_all_schedule(rule):
    data = await _get_json(f"{rule}/schedule")
    try:
        return data["results"]
    except KeyError as e:
        raise Spla3APIError("Spla3 API response did not include schedule results") from e
