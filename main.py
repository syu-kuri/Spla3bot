import asyncio
import asyncpg

from bot import Spla3Bot
from lib.config import *
from lib.discord import *

async def main():
    database = await asyncpg.create_pool(db_url, max_size=1, min_size=1)
    await database.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            user_id text unique,
            friend_code text NOT NULL
        );
    ''')
    bot = Spla3Bot(database=database)
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
        await database.close()
        await bot.logout()


if __name__ == '__main__':
    asyncio.run(main())
