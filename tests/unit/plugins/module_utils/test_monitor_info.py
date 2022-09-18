from .module_test_case import ModuleTestCase
import plugins.modules.monitor_info as module


class TestMonitorInfo(ModuleTestCase):
    def setUp(self):
        super(TestMonitorInfo, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None
        }
        self.monitor_id_1 = self.add_monitor("monitor 1")
        self.monitor_id_2 = self.add_monitor("monitor 2")

    def test_all_monitors(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        monitor_ids = [self.monitor_id_1, self.monitor_id_2]
        self.assertEqual(len(result["monitors"]), len(monitor_ids))
        self.assertEqual([i["id"] for i in result["monitors"]], monitor_ids)

    def test_monitor_by_id(self):
        self.params["id"] = self.monitor_id_2
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["monitors"]), 1)
        self.assertEqual(result["monitors"][0]["id"], self.monitor_id_2)

    def test_monitor_by_name(self):
        name = "monitor 2"
        self.params["name"] = name
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["monitors"]), 1)
        self.assertEqual(result["monitors"][0]["name"], name)
