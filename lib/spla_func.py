from lib.api import *
from lib.check import *
from lib.molding import *


def spla3(rule, time_slot):
    if time_slot != "schedule":
        if rule != "coop-grouping-regular":
            base = get_schedule(rule, time_slot)
            data = check_fest(base, time_slot)
        else:
            base = get_schedule(rule, time_slot)
            data = common_coop_molding(base)
    return data