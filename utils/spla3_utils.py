from typing import Dict

import requests

from config.config import USER_AGENT
from constants.common import StatusCode
from constants.message import APIMessage
from utils.log_util import LogUtil


class Spla3Util:
    @classmethod
    def get_headers(cls) -> Dict:
        """
        Get headers for api request.

        :return: headers
        """
        headers = {
            'User-Agent': USER_AGENT
        }

        return headers

    @classmethod
    def fetch_schedule(cls, url: str) -> Dict:
        """
        Fetch splatoon 3 Schedule from API.

        :param url: API request url
        :return: Schedule data
        """
        try:
            res = requests.api.get(url, headers=cls.get_headers())

            status_code = res.status_code

            if status_code == StatusCode.SUCCESS:
                # SCCESS
                LogUtil.info(APIMessage.AI0000000001)

                if 'results' in res.json():
                    return res.json()['results']
                elif 'result' in res.json():
                    return res.json()['result']
            else:
                # other
                LogUtil.warn(APIMessage.AW0000000001.format(status_code))

                return {}
        except Exception as e:
            LogUtil.exception(APIMessage.AE0000000001.format(e))

            return {}
