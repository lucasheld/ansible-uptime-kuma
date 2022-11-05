from .module_test_case import ModuleTestCase
import plugins.modules.settings_info as module


class TestSettingsInfo(ModuleTestCase):
    def setUp(self):
        super(TestSettingsInfo, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None
        }

    def test_settings(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["settings"]), 10)
