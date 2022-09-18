from .module_test_case import ModuleTestCase
import plugins.modules.proxy as module
from plugins.module_utils.common import get_proxy_by_host_port

from uptime_kuma_api import ProxyProtocol


class TestProxy(ModuleTestCase):
    def setUp(self):
        super(TestProxy, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "host": None,
            "port": None,
            "protocol": None,
            "auth": None,
            "username": None,
            "password": None,
            "active": None,
            "default": None,
            "applyExisting": None,
            "state": "present"
        }

    def test_proxy(self):
        # add proxy by name
        self.params.update({
            "protocol": ProxyProtocol.HTTP,
            "host": "127.0.0.1",
            "port": 8080,
            "auth": True,
            "username": "username",
            "password": "password",
            "active": True,
            "default": False
        })

        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        proxy = get_proxy_by_host_port(self.api, self.params["host"], self.params["port"])
        self.assertEqual(proxy["auth"], self.params["auth"])
        self.assertEqual(proxy["username"], self.params["username"])
        self.assertEqual(proxy["password"], self.params["password"])
        self.assertEqual(proxy["active"], self.params["active"])
        self.assertEqual(proxy["default"], self.params["default"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # edit proxy by id
        proxy_id = proxy["id"]
        self.params.update({
            "id": proxy_id,
            "name": None,
            "protocol": ProxyProtocol.HTTPS,
            "host": "127.0.0.2",
            "port": 8888
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        proxy = self.api.get_proxy(proxy_id)
        self.assertEqual(proxy["protocol"], self.params["protocol"])
        self.assertEqual(proxy["host"], self.params["host"])
        self.assertEqual(proxy["port"], self.params["port"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # delete proxy
        self.params.update({
            "state": "absent",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
