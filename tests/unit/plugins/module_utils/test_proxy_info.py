from .module_test_case import ModuleTestCase
import plugins.modules.proxy_info as module


class TestProxyInfo(ModuleTestCase):
    def setUp(self):
        super(TestProxyInfo, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "host": None,
            "port": None
        }
        self.proxy_id_1 = self.add_proxy(host="127.0.0.1")
        self.proxy_id_2 = self.add_proxy(host="127.0.0.2")

    def test_all_proxies(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        proxy_ids = [self.proxy_id_1, self.proxy_id_2]
        self.assertEqual(len(result["proxies"]), len(proxy_ids))
        self.assertEqual([i["id"] for i in result["proxies"]], proxy_ids)

    def test_proxy_by_id(self):
        self.params["id"] = self.proxy_id_2
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["proxies"]), 1)
        self.assertEqual(result["proxies"][0]["id"], self.proxy_id_2)

    def test_proxy_by_host_port(self):
        host = "127.0.0.2"
        port = 8080
        self.params["host"] = host
        self.params["port"] = port
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["proxies"]), 1)
        self.assertEqual(result["proxies"][0]["host"], host)
        self.assertEqual(result["proxies"][0]["port"], port)
