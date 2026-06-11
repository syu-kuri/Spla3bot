import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class ConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class Settings:
    token: str
    prefix: str
    error_channel_id: int
    test_guilds: str | None = None


def _get_required(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


def _get_required_int(name: str) -> int:
    value = _get_required(name)
    try:
        return int(value)
    except ValueError as e:
        raise ConfigError(f"Environment variable {name} must be an integer") from e


def load_settings() -> Settings:
    return Settings(
        token=_get_required("token"),
        prefix=_get_required("prefix"),
        error_channel_id=_get_required_int("error_ch"),
        test_guilds=os.getenv("test_guilds"),
    )


settings = load_settings()

# Backward-compatible exports for existing modules. Prefer `settings` in new code.
token = settings.token
prefix = settings.prefix
error_ch = settings.error_channel_id
test_guilds = settings.test_guilds

__all__ = [
    "ConfigError",
    "Settings",
    "settings",
    "token",
    "prefix",
    "error_ch",
    "test_guilds",
]
