from .module_test_case import ModuleTestCase
import plugins.modules.notification_info as module


class TestNotificationInfo(ModuleTestCase):
    def setUp(self):
        super(TestNotificationInfo, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None
        }
        self.notification_id_1 = self.add_notification("notification 1")
        self.notification_id_2 = self.add_notification("notification 2")

    def test_all_notifications(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        notification_ids = [self.notification_id_1, self.notification_id_2]
        self.assertEqual(len(result["notifications"]), len(notification_ids))
        self.assertEqual([i["id"] for i in result["notifications"]], notification_ids)

    def test_notification_by_id(self):
        self.params["id"] = self.notification_id_2
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["notifications"]), 1)
        self.assertEqual(result["notifications"][0]["id"], self.notification_id_2)

    def test_notification_by_name(self):
        name = "notification 2"
        self.params["name"] = name
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["notifications"]), 1)
        self.assertEqual(result["notifications"][0]["name"], name)
