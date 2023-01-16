from urllib import parse

import pyotp

from .module_test_case import ModuleTestCase
import plugins.modules.login as module


def parse_secret(uri):
    query = parse.urlsplit(uri).query
    params = dict(parse.parse_qsl(query))
    return params["secret"]


def generate_token(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()


class TestLogin(ModuleTestCase):
    def setUp(self):
        super(TestLogin, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_2fa": None
        }

    def test_login(self):
        self.params["api_username"] = self.username
        self.params["api_password"] = self.password

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])
        self.assertIsNotNone(result["token"])

    def test_login_with_2fa(self):
        self.params["api_username"] = self.username
        self.params["api_password"] = self.password

        # prepare 2fa
        r = self.api.prepare_2fa(self.password)
        uri = r["uri"]
        secret = parse_secret(uri)

        # verify token
        token = generate_token(secret)
        r = self.api.verify_token(token, self.password)
        self.assertEqual(r["valid"], True)

        # save 2fa
        r = self.api.save_2fa(self.password)
        self.assertEqual(r["msg"], "2FA Enabled.")

        # run module
        self.params["api_2fa"] = token
        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])
        self.assertIsNotNone(result["token"])

        # disable 2fa
        r = self.api.disable_2fa(self.password)
        self.assertEqual(r["msg"], "2FA Disabled.")
