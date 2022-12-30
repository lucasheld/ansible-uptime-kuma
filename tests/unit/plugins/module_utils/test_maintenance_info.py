from packaging.version import parse as parse_version
import plugins.modules.maintenance_info as module
from .module_test_case import ModuleTestCase


class TestMaintenanceInfo(ModuleTestCase):
    def setUp(self):
        super(TestMaintenanceInfo, self).setUp()

        if parse_version(self.api.version) < parse_version("1.19"):
            super(TestMaintenanceInfo, self).tearDown()
            self.skipTest("Unsupported in this Uptime Kuma version")

        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "title": None
        }
        self.maintenance_id_1 = self.add_maintenance("maintenance 1")
        self.maintenance_id_2 = self.add_maintenance("maintenance 2")

    def test_all_maintenances(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        maintenance_ids = [self.maintenance_id_1, self.maintenance_id_2]
        self.assertEqual(len(result["maintenances"]), len(maintenance_ids))
        self.assertEqual([i["id"] for i in result["maintenances"]], maintenance_ids)

    def test_maintenance_by_id(self):
        self.params["id"] = self.maintenance_id_2
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["maintenances"]), 1)
        self.assertEqual(result["maintenances"][0]["id"], self.maintenance_id_2)

    def test_maintenance_by_title(self):
        title = "maintenance 2"
        self.params["title"] = title
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["maintenances"]), 1)
        self.assertEqual(result["maintenances"][0]["title"], title)
