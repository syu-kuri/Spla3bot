import io
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from discord import app_commands
from PIL import Image

from cogs.spla3 import Spla3Cog
from lib.api import Spla3APIError
from lib.models import BattleStage


class StageImageTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.cog = Spla3Cog(MagicMock())
        self.interaction = SimpleNamespace(
            response=SimpleNamespace(defer=AsyncMock()),
            followup=SimpleNamespace(send=AsyncMock()),
        )
        self.rule = app_commands.Choice(name="ナワバリ", value="regular")
        self.schedule = BattleStage(
            is_fest=False,
            start_time="12:00",
            end_time="14:00",
            rule_name="ナワバリバトル",
            stages=["ステージA", "ステージB"],
            image_urls=["https://example.com/first.png", "https://example.com/second.png"],
        )
        client_session = self.enterContext(patch("lib.img.aiohttp.ClientSession"))
        session = MagicMock()
        client_session.return_value.__aenter__.return_value = session
        self.image_request = session.get.return_value
        self.image_response = MagicMock(read=AsyncMock())
        self.image_request.__aenter__.return_value = self.image_response

    async def run_stage(self):
        await self.cog.stage3.callback(self.cog, self.interaction, self.rule, None)
        self.interaction.followup.send.assert_awaited_once()
        return self.interaction.followup.send.await_args.kwargs

    def assert_schedule_fields(self, embed):
        fields = {field.name: field.value for field in embed.fields}
        self.assertIn("12:00 ～ 14:00", fields["開催時間"])
        self.assertIn("ステージA\nステージB", fields["ステージ"])

    @patch("cogs.spla3.spla3")
    async def test_image_failures_keep_schedule(self, get_schedule):
        get_schedule.return_value = self.schedule

        for failure in ("timeout", "404", "invalid image"):
            with self.subTest(failure=failure):
                self.interaction.followup.send.reset_mock()
                self.image_request.__aenter__.side_effect = TimeoutError if failure == "timeout" else None
                self.image_response.status = 404 if failure == "404" else 200
                self.image_response.read.return_value = b"not an image"

                message = await self.run_stage()
                self.assert_schedule_fields(message["embed"])
                self.assertIsNone(message["embed"].image.url)
                self.assertNotIn("file", message)

    @patch("cogs.spla3.spla3")
    async def test_success_attaches_combined_image(self, get_schedule):
        get_schedule.return_value = self.schedule
        self.image_response.status = 200
        with io.BytesIO() as buffer, Image.new("RGB", (3, 2)) as image:
            image.save(buffer, format="PNG")
            self.image_response.read.return_value = buffer.getvalue()

        message = await self.run_stage()
        self.assert_schedule_fields(message["embed"])
        self.assertEqual(message["embed"].image.url, "attachment://image.png")
        attachment = message["file"]
        try:
            with Image.open(attachment.fp) as image:
                self.assertEqual(image.size, (6, 2))
        finally:
            attachment.close()

    @patch("cogs.spla3.spla3", side_effect=Spla3APIError)
    async def test_schedule_failure_asks_user_to_retry(self, get_schedule):
        with self.assertLogs("cogs.spla3", level="WARNING"):
            message = await self.run_stage()
        self.assertEqual(message["embed"].title, "ステージ情報を取得できませんでした")
        self.assertIn("再度お試しください", message["embed"].description)
        self.assertNotIn("file", message)
