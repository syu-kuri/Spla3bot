import asyncio
import io

import aiohttp
from PIL import Image


IMAGE_TIMEOUT = aiohttp.ClientTimeout(total=10)


class ImageFetchError(RuntimeError):
    pass


def get_rule_image(rule_name):
    rule_images = {
        "ナワバリバトル": "https://images-ext-1.discordapp.net/external/sNH8hPsRSuUYU7eMhUebaL7v8I3q82OepAd-vN_5sWE/https/www.nintendo.co.jp/switch/aab6a/assets/images/battle-sec01_logo.png",
        "バンカラマッチ": "https://media.discordapp.net/attachments/808221718106603540/812571951872081920/battle-sec02_logo.png",
        "サーモンラン": "https://cdn.discordapp.com/attachments/808221718106603540/1021002540193685554/unknown.png",
        "ガチエリア": "https://cdn.discordapp.com/attachments/808221718106603540/815038217400090634/show.png",
        "ガチヤグラ": "https://cdn.discordapp.com/attachments/808221718106603540/815038610101370980/show.png",
        "ガチホコバトル": "https://cdn.discordapp.com/attachments/808221718106603540/815040449055162368/show.png",
        "ガチアサリ": "https://cdn.discordapp.com/attachments/808221718106603540/815040479166595092/show.png"
    }
    return rule_images.get(rule_name)


async def _fetch_image_bytes(session: aiohttp.ClientSession, url: str) -> bytes:
    try:
        async with session.get(url) as response:
            if response.status != 200:
                raise ImageFetchError(f"Image request returned HTTP {response.status}")
            return await response.read()
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        raise ImageFetchError("Failed to request stage image") from e


async def get_concat_h_cut(url1, url2):
    async with aiohttp.ClientSession(timeout=IMAGE_TIMEOUT) as session:
        image_bytes1, image_bytes2 = await asyncio.gather(
            _fetch_image_bytes(session, url1),
            _fetch_image_bytes(session, url2),
        )

    with Image.open(io.BytesIO(image_bytes1)) as img1, Image.open(io.BytesIO(image_bytes2)) as img2:
        img1 = img1.convert("RGB")
        img2 = img2.convert("RGB")
        dst = Image.new("RGB", (img1.width + img2.width, min(img1.height, img2.height)))
        dst.paste(img1, (0, 0))
        dst.paste(img2, (img1.width, 0))
        return dst
