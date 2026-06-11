from lib.api import get_schedule
from lib.check import check_fest
from lib.models import StageInfo
from lib.molding import common_coop_molding


COOP_RULES = {"coop-grouping", "coop-grouping-regular"}


async def spla3(rule, time_slot) -> StageInfo:
    if time_slot != "schedule":
        if rule in COOP_RULES:
            base = await get_schedule(rule, time_slot)
            data = common_coop_molding(base)
        else:
            base = await get_schedule(rule, time_slot)
            data = await check_fest(base, time_slot)
    return data
