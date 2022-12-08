import datetime

def time_molding(p1):
    _time = datetime.datetime.strptime(p1, '%Y-%m-%dT%H:%M:%S%z')
    time = _time.strftime('%m/%d %H:%M')
    return time

def common_molding(f):
    is_fest = f["is_fest"]
    st = f["start_time"]
    et = f["end_time"]
    rule_name = f["rule"]["name"]
    stages = []
    imgs = []
    for stage in f["stages"]:
        stages.append(stage["name"])
        imgs.append(stage["image"])

    start_time = time_molding(st)
    end_time = time_molding(et)

    return [is_fest, start_time, end_time, rule_name, stages, imgs]

def common_coop_molding(f):
    st = f["start_time"]
    et = f["end_time"]
    is_big_run = f["is_big_run"]
    stage = f["stage"]["name"]
    image = f["stage"]["image"]

    start_time = time_molding(st)
    end_time = time_molding(et)

    weapons = []
    for weapon in f["weapons"]:
        weapons.append(weapon["name"])

    return[is_big_run, start_time, end_time, stage, image, weapons]


def fest_molding(f):
    st = f["start_time"]
    et = f["end_time"]
    is_fest = f["is_fest"]
    is_tricolor = f["is_tricolor"]
    rule_name = f["rule"]["name"]
    stages = []
    imgs = []
    for stage in f["stages"]:
        stages.append(stage["name"])
        imgs.append(stage["image"])

    start_time = time_molding(st)
    end_time = time_molding(et)

    return [is_fest, is_tricolor, start_time, end_time, rule_name, stages, imgs]

def tricolor_molding(f):
    st = f["start_time"]
    et = f["end_time"]
    is_fest = f["is_fest"]
    is_tricolor = f["is_tricolor"]
    rule_name = f["rule"]["name"]
    stages = []
    for stage in f["stages"]:
        stages.append(stage["name"])
    tc_stage = f["tricolor_stage"]["name"]
    tc_img = f["tricolor_stage"]["image"]

    start_time = time_molding(st)
    end_time = time_molding(et)

    return [is_fest, is_tricolor, start_time, end_time, rule_name, stages, tc_stage, tc_img]