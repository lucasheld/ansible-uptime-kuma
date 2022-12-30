from .module_test_case import ModuleTestCase
import plugins.modules.settings as module


class TestSettings(ModuleTestCase):
    def setUp(self):
        super(TestSettings, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "password": None,
            "checkUpdate": None,
            "checkBeta": None,
            "keepDataPeriodDays": None,
            "serverTimezone": None,
            "entryPage": None,
            "searchEngineIndex": None,
            "primaryBaseURL": None,
            "steamAPIKey": None,
            "dnsCache": None,
            "tlsExpiryNotifyDays": None,
            "disableAuth": None,
            "trustProxy": None,
        }

    def test_settings(self):
        self.params.update({
            "checkBeta": True
        })

        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        settings = self.api.get_settings()
        self.assertEqual(settings["checkBeta"], self.params["checkBeta"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])
