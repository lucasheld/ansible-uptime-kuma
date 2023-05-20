from .module_test_case import ModuleTestCase
import plugins.modules.game_list_info as module


class TestGameListInfo(ModuleTestCase):
    def setUp(self):
        super(TestGameListInfo, self).setUp()

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
