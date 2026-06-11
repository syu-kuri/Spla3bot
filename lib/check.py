from lib.api import get_schedule
from lib.molding import common_molding, fest_molding, tricolor_molding

def check_fest(data, time_slot):
    if data["is_fest"]:
        fest_data = get_schedule("fest", time_slot)
        if fest_data["is_tricolor"]:
            return tricolor_molding(fest_data)
        else:
            return fest_molding(fest_data)
    else:
        return common_molding(data)
