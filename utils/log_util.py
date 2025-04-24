import logging
import io
import os
import sys


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class LogUtil:
    @classmethod
    def get_logger(cls) -> logging.Logger:
        logger = logging.getLogger('spla3bot')
        return logger

    @classmethod
    def get_hostname(cls) -> str:
        return os.environ.get('HOSTNAME', '(no host name)')

    @classmethod
    def get_user(cls):
        try:
            return '(no user)'
        except Exception as e:
            return '(no user)'

    @classmethod
    def debug(cls, message: str) -> None:
        logger = cls.get_logger()
        logger.debug(message, stack_info=False)

    @classmethod
    def info(cls, message: str) -> None:
        logger = cls.get_logger()
        logger.info(message, stack_info=False)

    @classmethod
    def warn(cls, message: str) -> None:
        logger = cls.get_logger()
        logger.warning(message, stack_info=False)

    @classmethod
    def error(cls, message: str) -> None:
        logger = cls.get_logger()
        logger.error(message, stack_info=False)

    @classmethod
    def exception(cls, message: str) -> None:
        logger = cls.get_logger()
        logger.exception(message)

    @classmethod
    def critical(cls, message: str) -> None:
        logger = cls.get_logger()
        logger.critical(message, exc_info=True)
