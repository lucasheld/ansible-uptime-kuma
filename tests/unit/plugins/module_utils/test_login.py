from .module_test_case import ModuleTestCase
import plugins.modules.login as module


class TestLogin(ModuleTestCase):
    def setUp(self):
        super(TestLogin, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None
        }

    def test_login(self):
        self.params["api_username"] = self.username
        self.params["api_password"] = self.password

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])
        self.assertIsNotNone(result["token"])
