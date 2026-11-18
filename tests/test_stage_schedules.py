import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from discord import app_commands

from cogs.spla3 import Spla3Cog
from lib.api import API_BASE_URL
from lib.img import ImageFetchError


FIXTURES = Path(__file__).with_name("fixtures")
RULE_NAMES = {"regular": "ナワバリ", "x": "Xマッチ", "coop-grouping": "サーモンラン"}


class StageScheduleTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.cog = Spla3Cog(MagicMock())
        self.payloads = json.loads((FIXTURES / "stage_schedules.json").read_text(encoding="utf-8"))
        self.raw_responses = {}
        client_session = self.enterContext(patch("lib.api.aiohttp.ClientSession"))
        session = MagicMock()
        client_session.return_value.__aenter__.return_value = session
        session.get.side_effect = self.mock_request
        self.enterContext(patch("cogs.spla3.get_concat_h_cut", side_effect=ImageFetchError))

    def mock_request(self, url):
        path = url.removeprefix(API_BASE_URL)
        body = self.raw_responses[path] if path in self.raw_responses else json.dumps(self.payloads[path])

        async def read_json():
            return json.loads(body)

        request = MagicMock()
        request.__aenter__.return_value = SimpleNamespace(status=200, json=read_json)
        return request

    async def run_stage(self, rule="regular", time_slot="now"):
        interaction = SimpleNamespace(
            response=SimpleNamespace(defer=AsyncMock()),
            followup=SimpleNamespace(send=AsyncMock()),
        )
        rule_choice = app_commands.Choice(name=RULE_NAMES[rule], value=rule)
        time_choice = app_commands.Choice(name=time_slot, value=time_slot)
        await self.cog.stage3.callback(self.cog, interaction, rule_choice, time_choice)
        interaction.followup.send.assert_awaited_once()
        return interaction.followup.send.await_args.kwargs["embed"]

    def assert_retry(self, embed):
        self.assertEqual(embed.title, "ステージ情報を取得できませんでした")
        self.assertIn("再度お試しください", embed.description)

    async def test_invalid_result_shapes_ask_user_to_retry(self):
        cases = json.loads((FIXTURES / "invalid_stage_results.json").read_text(encoding="utf-8"))
        for label, payload in cases.items():
            with self.subTest(label=label):
                self.payloads["regular/now"] = payload
                self.assert_retry(await self.run_stage())

    async def test_invalid_json_asks_user_to_retry(self):
        for body in ('{"results":', b"\xff"):
            with self.subTest(body=body):
                self.raw_responses["regular/now"] = body
                self.assert_retry(await self.run_stage())

    async def test_invalid_fields_ask_user_to_retry(self):
        cases = [
            ("regular", "now", "regular/now", {"is_fest": "false"}),
            ("regular", "now", "regular/now", {"start_time": "tomorrow"}),
            ("regular", "now", "regular/now", {"end_time": 123}),
            ("regular", "now", "regular/now", {"rule": {"name": None}}),
            ("regular", "now", "regular/now", {"stages": []}),
            ("regular", "now", "regular/now", {"stages": [{"name": "stage"}]}),
            ("regular", "now", "regular/now", {"stages": [None, {}]}),
            ("regular", "next", "fest/next", {"is_tricolor": None}),
            ("regular", "next", "fest/next", {"is_fest": False}),
            ("x", "now", "fest/now", {"tricolor_stage": {"image": "https://example.com/stage.png"}}),
            ("coop-grouping", "now", "coop-grouping/now", {"is_big_run": 1}),
            ("coop-grouping", "now", "coop-grouping/now", {"weapons": [{"name": 42}]}),
        ]
        for rule, time_slot, path, overrides in cases:
            with self.subTest(path=path, overrides=overrides):
                original = self.payloads[path]["results"][0]
                self.payloads[path]["results"][0] = original | overrides
                try:
                    self.assert_retry(await self.run_stage(rule, time_slot))
                finally:
                    self.payloads[path]["results"][0] = original

    async def test_valid_schedules_keep_existing_display(self):
        cases = [
            (
                "regular", "now", "ナワバリ",
                {"開催時間": "11/18 12:00 ～ 11/18 14:00", "ステージ": "ユノハナ大渓谷\nゴンズイ地区"},
                None,
            ),
            (
                "regular", "next", "フェス開催中",
                {"フェスステージ": "マテガイ放水路\nヤガラ市場", "トリカラステージ": "現在トリカラは開催されていません"},
                None,
            ),
            (
                "x", "now", "フェス開催中",
                {"フェスステージ": "マテガイ放水路\nヤガラ市場", "トリカラステージ": "マヒマヒリゾート＆スパ"},
                "https://example.com/tricolor.png",
            ),
            (
                "coop-grouping", "now", "サーモンラン",
                {"ステージ": "アラマキ砦", "支給ブキ": "スプラシューター\nスプラローラー"},
                "https://example.com/coop.png",
            ),
        ]
        for rule, time_slot, title, expected_fields, image in cases:
            with self.subTest(rule=rule, time_slot=time_slot):
                embed = await self.run_stage(rule, time_slot)
                self.assertIn(title, embed.title)
                fields = {field.name: field.value for field in embed.fields}
                for name, value in expected_fields.items():
                    self.assertEqual(fields[name], f"```{value}```")
                self.assertEqual(embed.image.url, image)
