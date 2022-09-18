from .module_test_case import ModuleTestCase
import plugins.modules.tag_info as module


class TestTagInfo(ModuleTestCase):
    def setUp(self):
        super(TestTagInfo, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None
        }
        self.tag_id_1 = self.add_tag("tag 1")
        self.tag_id_2 = self.add_tag("tag 2")

    def test_all_tags(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        tag_ids = [self.tag_id_1, self.tag_id_2]
        self.assertEqual(len(result["tags"]), len(tag_ids))
        self.assertEqual([i["id"] for i in result["tags"]], tag_ids)

    def test_tag_by_id(self):
        self.params["id"] = self.tag_id_2
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["tags"]), 1)
        self.assertEqual(result["tags"][0]["id"], self.tag_id_2)

    def test_tag_by_name(self):
        name = "tag 2"
        self.params["name"] = name
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["tags"]), 1)
        self.assertEqual(result["tags"][0]["name"], name)
