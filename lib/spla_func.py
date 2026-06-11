from lib.api import get_schedule
from lib.check import check_fest
from lib.molding import common_coop_molding


COOP_RULES = {"coop-grouping", "coop-grouping-regular"}


def spla3(rule, time_slot):
    if time_slot != "schedule":
        if rule in COOP_RULES:
            base = get_schedule(rule, time_slot)
            data = common_coop_molding(base)
        else:
            base = get_schedule(rule, time_slot)
            data = check_fest(base, time_slot)
    return data
