import asyncio
from json import JSONDecodeError

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
    except (JSONDecodeError, UnicodeDecodeError) as e:
        raise Spla3APIError("Spla3 API response was not valid JSON") from e
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        raise Spla3APIError("Failed to request Spla3 API") from e


async def get_schedule(rule, time_slot):
    results = await _get_results(f"{rule}/{time_slot}")
    if not results or not isinstance(results[0], dict):
        raise Spla3APIError("Spla3 API response did not include a schedule entry")
    return results[0]


async def get_all_schedule(rule):
    return await _get_results(f"{rule}/schedule")


async def _get_results(path: str) -> list:
    data = await _get_json(path)
    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise Spla3APIError("Spla3 API response did not include a schedule results list")
    return data["results"]
