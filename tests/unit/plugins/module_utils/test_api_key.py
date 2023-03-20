from packaging.version import parse as parse_version

import plugins.modules.api_key as module
from plugins.module_utils.common import get_api_key_by_name
from .module_test_case import ModuleTestCase


class TestApiKey(ModuleTestCase):
    def setUp(self):
        super(TestApiKey, self).setUp()

        if parse_version(self.api.version) < parse_version("1.21"):
            super(TestApiKey, self).tearDown()
            self.skipTest("Unsupported in this Uptime Kuma version")

        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None,
            "expires": None,
            "active": None,
            "state": "present"
        }

    def test_api_key(self):
        # add api key by name
        self.params.update({
            "name": "api key 1",
            "expires": "2023-03-30 12:20:00",
            "active": True,
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        self.assertIsNotNone(result["key"])
        api_key = get_api_key_by_name(self.api, self.params["name"])
        self.assertEqual(api_key["expires"], self.params["expires"])
        self.assertEqual(api_key["active"], self.params["active"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # disable api key
        self.params.update({
            "state": "disabled",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])

        api_key = get_api_key_by_name(self.api, self.params["name"])
        self.assertFalse(api_key["active"])

        self.params.update({
            "active": False
        })
        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # enable api key
        self.params.update({
            "state": "enabled",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])

        api_key = get_api_key_by_name(self.api, self.params["name"])
        self.assertTrue(api_key["active"])

        self.params.update({
            "active": True
        })
        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # delete api key
        self.params.update({
            "state": "absent",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
