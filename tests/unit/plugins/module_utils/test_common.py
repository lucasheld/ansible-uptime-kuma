from uptime_kuma_api import UptimeKumaApi

from .module_test_case import ModuleTestCase
import plugins.modules.monitor_info as module_monitor_info


class TestCommon(ModuleTestCase):
    def setUp(self):
        super(TestCommon, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None
        }

    def test_auto_login(self):
        # disable auth
        self.api.set_settings(self.password, disableAuth=True)

        # logout
        self.api.logout()
        self.api.disconnect()
        self.api = UptimeKumaApi(self.url)

        params = {
            **self.params,
            "id": None,
            "name": None
        }
        result = self.run_module(module_monitor_info, params)
        self.assertFalse(result["changed"])
        self.assertIsNotNone(result["monitors"])

        # enable auth again
        self.api.set_settings(disableAuth=False)
