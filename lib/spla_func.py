from lib.requests import *
from lib.check import *
from lib.molding import *


def spla3(p1, p2):
    if p2 != "schedule":
        if p1 != "coop-grouping-regular":
            base = get_schedule(p1, p2)
            data = check_fest(base, p2)
        elif p1 == "coop-grouping-regular":
            base = base = get_schedule(p1, p2)
            data = common_coop_molding(base)
    return data