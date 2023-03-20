from packaging.version import parse as parse_version

import plugins.modules.api_key_info as module
from .module_test_case import ModuleTestCase


class TestApiKeyInfo(ModuleTestCase):
    def setUp(self):
        super(TestApiKeyInfo, self).setUp()

        if parse_version(self.api.version) < parse_version("1.21"):
            super(TestApiKeyInfo, self).tearDown()
            self.skipTest("Unsupported in this Uptime Kuma version")

        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None
        }
        self.api_key_id_1 = self.add_api_key("api key 1")
        self.api_key_id_2 = self.add_api_key("api key 2")

    def test_all_api_keys(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        api_key_ids = [self.api_key_id_1, self.api_key_id_2]
        self.assertEqual(len(result["api_keys"]), len(api_key_ids))
        self.assertEqual([i["id"] for i in result["api_keys"]], api_key_ids)

    def test_api_key_by_id(self):
        self.params["id"] = self.api_key_id_2
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["api_keys"]), 1)
        self.assertEqual(result["api_keys"][0]["id"], self.api_key_id_2)

    def test_api_key_by_name(self):
        name = "api key 2"
        self.params["name"] = name
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["api_keys"]), 1)
        self.assertEqual(result["api_keys"][0]["name"], name)
