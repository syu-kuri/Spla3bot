import datetime
from typing import TypeVar

from lib.api import Spla3APIError
from lib.models import BattleStage, CoopStage, FestStage, TricolorStage


FieldType = TypeVar("FieldType")


def _required_field(data: object, field: str, expected_type: type[FieldType]) -> FieldType:
    value = data.get(field) if isinstance(data, dict) else None
    if not isinstance(value, expected_type):
        raise Spla3APIError(f"Invalid schedule field: {field}")
    return value


def _required_text(data: object, field: str) -> str:
    value = _required_field(data, field, str)
    if not value.strip():
        raise Spla3APIError(f"Empty schedule field: {field}")
    return value


def schedule_flag(data: object, field: str) -> bool:
    return _required_field(data, field, bool)


def time_molding(value: str) -> str:
    try:
        parsed_time = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError as e:
        raise Spla3APIError("Invalid schedule timestamp") from e
    return parsed_time.strftime("%m/%d %H:%M")


def _battle_stages(data: dict) -> list:
    stages = _required_field(data, "stages", list)
    if len(stages) < 2:
        raise Spla3APIError("Battle schedule requires at least two stages")
    return stages


def common_molding(data: dict) -> BattleStage:
    stages = _battle_stages(data)
    return BattleStage(
        is_fest=schedule_flag(data, "is_fest"),
        start_time=time_molding(_required_text(data, "start_time")),
        end_time=time_molding(_required_text(data, "end_time")),
        rule_name=_required_text(_required_field(data, "rule", dict), "name"),
        stages=[_required_text(stage, "name") for stage in stages],
        image_urls=[_required_text(stage, "image") for stage in stages],
    )


def common_coop_molding(data: dict) -> CoopStage:
    stage = _required_field(data, "stage", dict)
    weapons = _required_field(data, "weapons", list)
    return CoopStage(
        is_big_run=schedule_flag(data, "is_big_run"),
        start_time=time_molding(_required_text(data, "start_time")),
        end_time=time_molding(_required_text(data, "end_time")),
        stage=_required_text(stage, "name"),
        image_url=_required_text(stage, "image"),
        weapons=[_required_text(weapon, "name") for weapon in weapons],
    )


def fest_molding(data: dict) -> FestStage:
    stages = _battle_stages(data)
    return FestStage(
        is_fest=schedule_flag(data, "is_fest"),
        is_tricolor=schedule_flag(data, "is_tricolor"),
        start_time=time_molding(_required_text(data, "start_time")),
        end_time=time_molding(_required_text(data, "end_time")),
        rule_name=_required_text(_required_field(data, "rule", dict), "name"),
        stages=[_required_text(stage, "name") for stage in stages],
        image_urls=[_required_text(stage, "image") for stage in stages],
    )


def tricolor_molding(data: dict) -> TricolorStage:
    stages = _battle_stages(data)
    tricolor_stage = _required_field(data, "tricolor_stage", dict)
    return TricolorStage(
        is_fest=schedule_flag(data, "is_fest"),
        is_tricolor=schedule_flag(data, "is_tricolor"),
        start_time=time_molding(_required_text(data, "start_time")),
        end_time=time_molding(_required_text(data, "end_time")),
        rule_name=_required_text(_required_field(data, "rule", dict), "name"),
        stages=[_required_text(stage, "name") for stage in stages],
        tricolor_stage=_required_text(tricolor_stage, "name"),
        tricolor_image_url=_required_text(tricolor_stage, "image"),
    )
