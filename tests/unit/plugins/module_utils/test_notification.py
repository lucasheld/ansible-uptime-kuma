from .module_test_case import ModuleTestCase
import plugins.modules.notification as module
from plugins.module_utils.common import get_notification_by_name

from uptime_kuma_api import NotificationType


class TestNotification(ModuleTestCase):
    def setUp(self):
        super(TestNotification, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None,
            "isDefault": None,
            "applyExisting": None,
            "state": "present"
        }

    def test_notification(self):
        notification_name = "notification 1"

        # add notification by name
        self.params.update({
            "name": notification_name,
            "isDefault": True,
            "applyExisting": True,
            "type": NotificationType.PUSHBYTECHULUS,
            "pushAPIKey": "123456789"
        })

        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        notification = get_notification_by_name(self.api, self.params["name"])
        self.assertEqual(notification["isDefault"], self.params["isDefault"])
        self.assertEqual(notification["applyExisting"], self.params["applyExisting"])
        self.assertEqual(notification["type"], self.params["type"])
        self.assertEqual(notification["pushAPIKey"], self.params["pushAPIKey"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # edit notification by id
        notification_id = notification["id"]
        self.params.update({
            "id": notification_id,
            "name": None,
            "isDefault": False,
            "applyExisting": False,
            "type": NotificationType.PUSHDEER,
            "pushdeerKey": "987654321"
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        notification = self.api.get_notification(notification_id)
        self.assertEqual(notification["isDefault"], self.params["isDefault"])
        self.assertEqual(notification["applyExisting"], self.params["applyExisting"])
        self.assertEqual(notification["type"], self.params["type"])
        self.assertEqual(notification["pushdeerKey"], self.params["pushdeerKey"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # delete notification
        self.params.update({
            "state": "absent",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
