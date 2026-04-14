from lib.molding import *
from lib.api import *

def check_fest(data, time_slot):
    if data["is_fest"]:
        fest_data = get_schedule("fest", time_slot)
        if fest_data["is_tricolor"]:
            return tricolor_molding(fest_data)
        else:
            return fest_molding(fest_data)
    else:
        return common_molding(data)
