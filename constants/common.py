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
