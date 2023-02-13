from packaging.version import parse as parse_version
from .module_test_case import ModuleTestCase
import plugins.modules.game_list_info as module


class TestGameListInfo(ModuleTestCase):
    def setUp(self):
        super(TestGameListInfo, self).setUp()

        if parse_version(self.api.version) < parse_version("1.20"):
            super(TestGameListInfo, self).tearDown()
            self.skipTest("Unsupported in this Uptime Kuma version")

        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None
        }

    def test_game_list(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertTrue("keys" in result["game_list"][0])
