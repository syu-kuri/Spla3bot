import asyncio

from bot import Spla3Bot
from lib.config import *

async def main():
    bot = Spla3Bot()
    for file in os.listdir(f"./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.logout()


if __name__ == '__main__':
    asyncio.run(main())
