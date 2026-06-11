import datetime
from lib.models import BattleStage, CoopStage, FestStage, TricolorStage

def time_molding(p1):
    _time = datetime.datetime.strptime(p1, '%Y-%m-%dT%H:%M:%S%z')
    time = _time.strftime('%m/%d %H:%M')
    return time

def common_molding(f):
    is_fest = f["is_fest"]
    st = f["start_time"]
    et = f["end_time"]
    rule_name = f["rule"]["name"]
    stages = [stage["name"] for stage in f["stages"]]
    imgs = [stage["image"] for stage in f["stages"]]

    start_time = time_molding(st)
    end_time = time_molding(et)

    return BattleStage(
        is_fest=is_fest,
        start_time=start_time,
        end_time=end_time,
        rule_name=rule_name,
        stages=stages,
        image_urls=imgs,
    )

def common_coop_molding(f):
    st = f["start_time"]
    et = f["end_time"]
    is_big_run = f["is_big_run"]
    stage = f["stage"]["name"]
    image = f["stage"]["image"]

    start_time = time_molding(st)
    end_time = time_molding(et)

    weapons = [weapon["name"] for weapon in f["weapons"]]

    return CoopStage(
        is_big_run=is_big_run,
        start_time=start_time,
        end_time=end_time,
        stage=stage,
        image_url=image,
        weapons=weapons,
    )


def fest_molding(f):
    st = f["start_time"]
    et = f["end_time"]
    is_fest = f["is_fest"]
    is_tricolor = f["is_tricolor"]
    rule_name = f["rule"]["name"]
    stages = [stage["name"] for stage in f["stages"]]
    imgs = [stage["image"] for stage in f["stages"]]

    start_time = time_molding(st)
    end_time = time_molding(et)

    return FestStage(
        is_fest=is_fest,
        is_tricolor=is_tricolor,
        start_time=start_time,
        end_time=end_time,
        rule_name=rule_name,
        stages=stages,
        image_urls=imgs,
    )

def tricolor_molding(f):
    st = f["start_time"]
    et = f["end_time"]
    is_fest = f["is_fest"]
    is_tricolor = f["is_tricolor"]
    rule_name = f["rule"]["name"]
    stages = [stage["name"] for stage in f["stages"]]
    tc_stage = f["tricolor_stage"]["name"]
    tc_img = f["tricolor_stage"]["image"]

    start_time = time_molding(st)
    end_time = time_molding(et)

    return TricolorStage(
        is_fest=is_fest,
        is_tricolor=is_tricolor,
        start_time=start_time,
        end_time=end_time,
        rule_name=rule_name,
        stages=stages,
        tricolor_stage=tc_stage,
        tricolor_image_url=tc_img,
    )
