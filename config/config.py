import os
from typing import NamedTuple, Literal

from dotenv import load_dotenv


load_dotenv()


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


# Bot Infomation
version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=1, releaselevel='alpha', serial=0)

# log
Log_Format = "%(asctime)s, %(name)s, %(process)s, %(thread)s, %(funcName)s [%(levelname)s] %(message)s"

# Creator Infomation
CREATOR_NAME = os.environ.get('CREATOR_NAME', 'syukuri')

# Discord
TOKEN = os.environ.get('TOKEN', '')
PREFIX = os.environ.get('PREFIX', '!')
TEST_GUILDS = os.environ.get('test_guilds')
ERROR_CH = os.environ.get('ERROR_CH')

# API
SPLA3_BASE_URL = 'https://spla3.yuu26.com/api/'
USER_AGENT = os.environ.get('USER_AGENT', '').encode('utf-8')
