from lib.api import get_schedule
from lib.models import BattleStage, FestStage, TricolorStage
from lib.molding import common_molding, fest_molding, tricolor_molding

async def check_fest(data, time_slot) -> BattleStage | FestStage | TricolorStage:
    if data["is_fest"]:
        fest_data = await get_schedule("fest", time_slot)
        if fest_data["is_tricolor"]:
            return tricolor_molding(fest_data)
        else:
            return fest_molding(fest_data)
    else:
        return common_molding(data)
