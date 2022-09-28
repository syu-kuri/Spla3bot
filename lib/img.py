from PIL import Image
import requests

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

def get_concat_h_cut(url1, url2):
    response1 = requests.get(url1, stream=True)
    response2 = requests.get(url2, stream=True)
    response1.raw.decode_content = True
    response2.raw.decode_content = True
    img1 = Image.open(response1.raw)
    img2 = Image.open(response2.raw)
    dst = Image.new('RGB', (img1.width + img2.width, min(img1.height, img2.height)))
    dst.paste(img1, (0, 0))
    dst.paste(img2, (img1.width, 0))
    return dst