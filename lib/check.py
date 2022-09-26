from pprint import pprint
from lib.molding import *
from lib.requests import *

def check_fest(f, p1):
    if f["is_fest"]:
        _data = get_schedule("fest", p1)
        if _data["is_tricolor"]:
            # print("トリカラあり")
            data = tricolor_molding(_data)
            return data
        else:
            # print("トリカラなし")
            data = fest_molding(_data)
            return data
    else:
        data = common_molding(f)
        return data
