from .module_test_case import ModuleTestCase
import plugins.modules.monitor as module
from plugins.module_utils.common import get_monitor_by_name

from uptime_kuma_api import MonitorType


class TestMonitor(ModuleTestCase):
    def setUp(self):
        super(TestMonitor, self).setUp()
        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None,
            "description": None,
            "type": None,
            "interval": None,
            "retryInterval": None,
            "resendInterval": None,
            "maxretries": None,
            "upsideDown": None,
            "notificationIDList": None,
            "httpBodyEncoding": None,
            "notification_names": None,
            "url": None,
            "expiryNotification": None,
            "ignoreTls": None,
            "maxredirects": None,
            "accepted_statuscodes": None,
            "proxyId": None,
            "proxy": None,
            "method": None,
            "body": None,
            "headers": None,
            "authMethod": None,
            "tlsCert": None,
            "tlsKey": None,
            "tlsCa": None,
            "basic_auth_user": None,
            "basic_auth_pass": None,
            "authDomain": None,
            "authWorkstation": None,
            "keyword": None,
            "grpcUrl": None,
            "grpcEnableTls": None,
            "grpcServiceName": None,
            "grpcMethod": None,
            "grpcProtobuf": None,
            "grpcBody": None,
            "grpcMetadata": None,
            "hostname": None,
            "packetSize": None,
            "port": None,
            "dns_resolve_server": None,
            "dns_resolve_type": None,
            "mqttUsername": None,
            "mqttPassword": None,
            "mqttTopic": None,
            "mqttSuccessMessage": None,
            "databaseConnectionString": None,
            "databaseQuery": None,
            "docker_container": None,
            "docker_host": None,
            "docker_host_name": None,
            "radiusUsername": None,
            "radiusPassword": None,
            "radiusSecret": None,
            "radiusCalledStationId": None,
            "radiusCallingStationId": None,
            "game": None,
            "state": "present"
        }

    def test_monitor(self):
        notification_id_1 = self.add_notification()
        notification_id_2 = self.add_notification()

        # add monitor by name
        self.params.update({
            "type": MonitorType.HTTP,
            "name": "monitor 1",
            "interval": 60,
            "retryInterval": 60,
            "maxretries": 0,
            "notificationIDList": [notification_id_1, notification_id_2],
            "upsideDown": False,
            "url": "http://127.0.0.1",
            "resendInterval": 0
        })

        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        monitor = get_monitor_by_name(self.api, self.params["name"])
        self.assertEqual(monitor["type"], self.params["type"])
        self.assertEqual(monitor["interval"], self.params["interval"])
        self.assertEqual(monitor["retryInterval"], self.params["retryInterval"])
        self.assertEqual(monitor["maxretries"], self.params["maxretries"])
        self.assertEqual(monitor["notificationIDList"], self.params["notificationIDList"])
        self.assertEqual(monitor["upsideDown"], self.params["upsideDown"])
        self.assertEqual(monitor["url"], self.params["url"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # edit monitor by id
        monitor_id = monitor["id"]
        self.params.update({
            "id": monitor_id,
            "type": MonitorType.PING,
            "hostname": "127.0.0.10"
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        monitor = self.api.get_monitor(monitor_id)
        self.assertEqual(monitor["type"], self.params["type"])
        self.assertEqual(monitor["hostname"], self.params["hostname"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # pause monitor
        self.params.update({
            "state": "paused",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # resume monitor
        self.params.update({
            "state": "resumed",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # delete monitor
        self.params.update({
            "state": "absent",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
