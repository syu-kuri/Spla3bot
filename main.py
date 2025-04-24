import asyncio
import logging
import os
import sys

from bot import Spla3Bot
from config.config import TOKEN, Log_Format
from constants.message import Messages
from utils.log_util import LogUtil


async def main():
    bot = Spla3Bot()

    for file in os.listdir(f'./cogs'):
        if file == '__init__.py':
            continue

        if file.endswith('.py'):
            extension = file[:-3]
            try:
                await bot.load_extension(f'cogs.{extension}')
                LogUtil.info(Messages.BI0000000002.format(extension))
            except Exception as e:
                LogUtil.exception(Messages.BW0000000003.format(e))

    try:
        await bot.start(TOKEN)
    except Exception as e:
        LogUtil.exception(Messages.BE0000000001.format(e))


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[
            logging.FileHandler(
                filename='logs/app.log',
                encoding='utf-8',
                mode='a'
            ),
            logging.StreamHandler(
                stream=sys.stdout,
            )
        ],
        format=Log_Format,
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    asyncio.run(main())
