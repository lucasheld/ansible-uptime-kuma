from packaging.version import parse as parse_version
from uptime_kuma_api import MaintenanceStrategy

import plugins.modules.maintenance as module
from plugins.module_utils.common import get_maintenance_by_title
from .module_test_case import ModuleTestCase


class TestMaintenance(ModuleTestCase):
    def setUp(self):
        super(TestMaintenance, self).setUp()

        if parse_version(self.api.version) < parse_version("1.19"):
            super(TestMaintenance, self).tearDown()
            self.skipTest("Unsupported in this Uptime Kuma version")

        self.params = {
            "api_url": None,
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "title": None,
            "strategy": None,
            "active": None,
            "description": None,
            "dateRange": None,
            "intervalDay": None,
            "weekdays": None,
            "daysOfMonth": None,
            "timeRange": None,
            "monitors": None,
            "status_pages": None,
            "state": "present"
        }

    def test_maintenance(self):
        # add maintenance by name
        monitor_name = "monitor 1"
        monitor_id = self.add_monitor(monitor_name)

        status_page_title = "status_page 1"
        status_page_slug = "slug1"
        self.add_status_page(status_page_slug, status_page_title)
        # self.api.save_status_page(status_page_slug)
        status_page_id = self.api.get_status_page(status_page_slug)["id"]

        self.params.update({
            "title": "maintenance 1",
            "description": "test",
            "strategy": MaintenanceStrategy.SINGLE,
            "active": True,
            "intervalDay": 1,
            "dateRange": [
                "2022-12-27 22:36:00",
                "2022-12-29 22:36:00"
            ],
            "timeRange": [
                {
                    "hours": 2,
                    "minutes": 0,
                    "seconds": 0
                },
                {
                    "hours": 3,
                    "minutes": 0,
                    "seconds": 0
                }
            ],
            "weekdays": [],
            "daysOfMonth": [],
            "monitors": [
                {
                    "id": monitor_id,
                    "name": monitor_name
                }
            ],
            "status_pages": [
                {
                    "id": status_page_id,
                    "name": status_page_title
                }
            ]
        })

        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        maintenance = get_maintenance_by_title(self.api, self.params["title"])
        self.assertEqual(maintenance["description"], self.params["description"])
        self.assertEqual(maintenance["strategy"], self.params["strategy"])
        self.assertEqual(maintenance["active"], self.params["active"])
        self.assertEqual(maintenance["intervalDay"], self.params["intervalDay"])
        self.assertEqual(maintenance["dateRange"], self.params["dateRange"])
        self.assertEqual(maintenance["timeRange"], self.params["timeRange"])
        self.assertEqual(maintenance["weekdays"], self.params["weekdays"])
        self.assertEqual(maintenance["daysOfMonth"], self.params["daysOfMonth"])

        maintenance_id = maintenance["id"]
        maintenance_monitors = self.api.get_monitor_maintenance(maintenance_id)
        maintenance_status_pages = self.api.get_status_page_maintenance(maintenance_id)
        for maintenance_status_page in maintenance_status_pages:
            maintenance_status_page["name"] = maintenance_status_page.pop("title")
        self.assertEqual(maintenance_monitors, self.params["monitors"])
        self.assertEqual(maintenance_status_pages, self.params["status_pages"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # edit maintenance by id
        maintenance_id = maintenance["id"]
        self.params.update({
            "id": maintenance_id,
            "strategy": MaintenanceStrategy.RECURRING_INTERVAL,
            "dateRange": [
                "2022-12-27 22:37:00",
                "2022-12-31 22:37:00"
            ]
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        maintenance = self.api.get_maintenance(maintenance_id)
        self.assertEqual(maintenance["strategy"], self.params["strategy"])
        self.assertEqual(maintenance["dateRange"], self.params["dateRange"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # pause maintenance
        self.params.update({
            "state": "paused",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # resume maintenance
        self.params.update({
            "state": "resumed",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # delete maintenance
        self.params.update({
            "state": "absent",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
