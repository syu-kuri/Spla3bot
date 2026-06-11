# Spla3bot

Discord bot for Splatoon 3 stage information.

## Docker

Create `.env` from the example and set your Discord bot values.

```sh
cp .env.example .env
```

Build and start the bot.

```sh
docker compose up -d --build
```

Show logs.

```sh
docker compose logs -f spla3bot
```

Stop the bot.

```sh
docker compose down
```
