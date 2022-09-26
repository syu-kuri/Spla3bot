def get_rule_color(p1: str):
    rule_colors = {
        "ナワバリバトル": 0x7eff00,
        "フェスバトル": 0xA281B7,
        "サーモンラン": 0xf02c7d,
        "ガチエリア": 0xff7213,
        "ガチヤグラ": 0xff7213,
        "ガチホコバトル": 0xff7213,
        "ガチアサリ": 0xff7213
    }
    return rule_colors.get(p1)