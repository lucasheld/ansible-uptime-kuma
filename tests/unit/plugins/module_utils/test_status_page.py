from packaging.version import parse as parse_version

import plugins.modules.status_page as module
from .module_test_case import ModuleTestCase


class TestStatusPage(ModuleTestCase):
    def setUp(self):
        super(TestStatusPage, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "slug": None,
            "title": None,
            "description": None,
            "theme": None,
            "published": None,
            "showTags": None,
            "domainNameList": None,
            "customCSS": None,
            "footerText": None,
            "showPoweredBy": None,
            "icon": None,
            "publicGroupList": None,
            "incident": None,
            "state": "present"
        }

    def test_status_page(self):
        slug = "slug1"

        # add status page
        monitor_id = self.add_monitor()
        self.params.update({
            "slug": slug,
            "title": "status page 1",
            "description": "description 1",
            "theme": "light",
            "published": True,
            "showTags": False,
            "domainNameList": [],
            "customCSS": "",
            "footerText": None,
            "showPoweredBy": False,
            "icon": "/icon.svg",
            "publicGroupList": [
                {
                    'name': 'Services',
                    'weight': 1,
                    'monitorList': [
                        {
                            "id": monitor_id,
                            "name": None
                        }
                    ]
                }
            ]
        })

        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        status_page = self.api.get_status_page(slug)
        self.assertEqual(status_page["title"], self.params["title"])
        self.assertEqual(status_page["description"], self.params["description"])
        self.assertEqual(status_page["theme"], self.params["theme"])
        self.assertEqual(status_page["published"], self.params["published"])
        self.assertEqual(status_page["showTags"], self.params["showTags"])
        self.assertEqual(status_page["domainNameList"], self.params["domainNameList"])
        self.assertEqual(status_page["customCSS"], self.params["customCSS"])
        self.assertEqual(status_page["footerText"], self.params["footerText"])
        self.assertEqual(status_page["showPoweredBy"], self.params["showPoweredBy"])
        self.assertEqual(status_page["icon"], self.params["icon"])
        public_group_list = status_page["publicGroupList"]
        for i in public_group_list:
            del i["id"]
            for j in i.get("monitorList", []):
                j.pop("sendUrl", None)
                j["name"] = None
                if parse_version("1.19") <= parse_version(self.api.version) < parse_version("1.19.5"):
                    j.pop("maintenance")
        self.assertEqual(public_group_list, self.params["publicGroupList"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # edit status page
        self.params.update({
            "title": "status page 1 new",
            "theme": "dark"
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        status_page = self.api.get_status_page(slug)
        self.assertEqual(status_page["title"], self.params["title"])
        self.assertEqual(status_page["theme"], self.params["theme"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # delete status page
        self.params.update({
            "state": "absent",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
