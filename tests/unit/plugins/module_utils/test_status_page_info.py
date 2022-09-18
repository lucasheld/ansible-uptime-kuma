from .module_test_case import ModuleTestCase
import plugins.modules.status_page_info as module


class TestStatusPageInfo(ModuleTestCase):
    def setUp(self):
        super(TestStatusPageInfo, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "slug": None
        }
        self.add_status_page("slug1")
        self.add_status_page("slug2")

    def test_all_status_pages(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        status_page_slugs = ["slug1", "slug2"]
        self.assertEqual(len(result["status_pages"]), len(status_page_slugs))
        self.assertEqual([i["slug"] for i in result["status_pages"]], status_page_slugs)

    def test_status_page_by_slug(self):
        self.params["slug"] = "slug2"
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["status_pages"]), 1)
        self.assertEqual(result["status_pages"][0]["slug"], "slug2")
