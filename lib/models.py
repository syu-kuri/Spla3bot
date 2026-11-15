from dataclasses import dataclass


@dataclass(frozen=True)
class BattleStage:
    is_fest: bool
    start_time: str
    end_time: str
    rule_name: str
    stages: list[str]
    image_urls: list[str]


@dataclass(frozen=True)
class FestStage:
    is_fest: bool
    is_tricolor: bool
    start_time: str
    end_time: str
    rule_name: str
    stages: list[str]
    image_urls: list[str]


@dataclass(frozen=True)
class TricolorStage:
    is_fest: bool
    is_tricolor: bool
    start_time: str
    end_time: str
    rule_name: str
    stages: list[str]
    tricolor_stage: str
    tricolor_image_url: str


@dataclass(frozen=True)
class CoopStage:
    is_big_run: bool
    start_time: str
    end_time: str
    stage: str
    image_url: str
    weapons: list[str]


StageInfo = BattleStage | FestStage | TricolorStage | CoopStage
