from .module_test_case import ModuleTestCase
import plugins.modules.setup as module


class TestSetup(ModuleTestCase):
    def setUp(self):
        super(TestSetup, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None
        }

    def test_setup(self):
        self.params.update({
            "api_username": self.username,
            "api_password": self.password
        })

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])
