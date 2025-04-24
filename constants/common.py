class StatusCode:
    SUCCESS = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class EmbedColor:
    TURF_WAR = 0x7eff00
    IS_FEST = 0xA281B7
    COOP = 0xf02c7d
    AREA = 0xff7213
    LOFT = 0xff7213
    GOAL = 0xff7213
    CLAM = 0xff7213

    LIST = {
        'TURF_WAR': TURF_WAR,
        'AREA': AREA,
        'LOFT': LOFT,
        'GOAL': GOAL,
        'CLAM': CLAM,
    }

class MatchLogoPath:
    TURF_WAR = "https://images-ext-1.discordapp.net/external/sNH8hPsRSuUYU7eMhUebaL7v8I3q82OepAd-vN_5sWE/https/www.nintendo.co.jp/switch/aab6a/assets/images/battle-sec01_logo.png"
    COOP = "https://cdn.discordapp.com/attachments/808221718106603540/1021002540193685554/unknown.png"
    AREA = "https://cdn.discordapp.com/attachments/808221718106603540/815038217400090634/show.png"
    LOFT = "https://cdn.discordapp.com/attachments/808221718106603540/815038610101370980/show.png"
    GOAL = "https://cdn.discordapp.com/attachments/808221718106603540/815040449055162368/show.png"
    CLAM = "https://cdn.discordapp.com/attachments/808221718106603540/815040479166595092/show.png"

    LIST = {
        'AREA': AREA,
        'COOP': COOP,
        'CLAM': CLAM,
        'TURF_WAR': TURF_WAR,
        'LOFT': LOFT,
        'GOAL': GOAL,
    }
