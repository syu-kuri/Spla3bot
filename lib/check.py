from lib.api import Spla3APIError, get_schedule
from lib.models import BattleStage, FestStage, TricolorStage
from lib.molding import common_molding, fest_molding, schedule_flag, tricolor_molding


async def check_fest(data: dict, time_slot: str) -> BattleStage | FestStage | TricolorStage:
    if not schedule_flag(data, "is_fest"):
        return common_molding(data)

    fest_data = await get_schedule("fest", time_slot)
    if not schedule_flag(fest_data, "is_fest"):
        raise Spla3APIError("Expected a Splatfest entry in the schedule")
    if schedule_flag(fest_data, "is_tricolor"):
        return tricolor_molding(fest_data)
    return fest_molding(fest_data)
