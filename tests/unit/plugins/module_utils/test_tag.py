from .module_test_case import ModuleTestCase
import plugins.modules.tag as module
from plugins.module_utils.common import get_tag_by_name


class TestTag(ModuleTestCase):
    def setUp(self):
        super(TestTag, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None,
            "color": None,
            "state": "present"
        }

    def test_tag(self):
        # add tag by name
        self.params.update({
            "name": "tag 1",
            "color": "#ffffff"
        })

        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        tag = get_tag_by_name(self.api, self.params["name"])
        self.assertEqual(tag["color"], self.params["color"])

        # edit tag by id
        tag_id = tag["id"]
        self.params.update({
            "id": tag_id,
            "color": "#000000"
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        tag = self.api.get_tag(tag_id)
        self.assertEqual(tag["color"], self.params["color"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # delete tag
        self.params.update({
            "state": "absent",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
