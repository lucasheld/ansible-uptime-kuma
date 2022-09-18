import json

from .module_test_case import ModuleTestCase
import plugins.modules.monitor_tag as module
from plugins.module_utils.common import get_monitor_tag


class TestMonitorTag(ModuleTestCase):
    def setUp(self):
        super(TestMonitorTag, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "monitor_id": None,
            "tag_id": None,
            "monitor_name": None,
            "tag_name": None,
            "value": None,
            "state": "present"
        }

    def test_monitor_tag(self):
        monitor_name = "monitor 1"
        tag_name = "tag 1"
        value = "value 1"
        monitor_id = self.add_monitor(monitor_name)
        tag_id = self.add_tag(tag_name)

        # add monitor tag by monitor name and tag name
        self.params.update({
            "monitor_name": monitor_name,
            "tag_name": tag_name,
            "value": value
        })

        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        monitor = self.api.get_monitor(monitor_id)
        tag = self.api.get_tag(tag_id)
        monitor_tag = get_monitor_tag(monitor, tag, value)
        self.assertEqual(monitor_tag["value"], self.params["value"])

        # add monitor tag by monitor id and tag id again
        self.params.update({
            "monitor_id": monitor_id,
            "tag_id": tag_id,
            "value": value
        })
        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # delete monitor tag
        self.params.update({
            "state": "absent",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
