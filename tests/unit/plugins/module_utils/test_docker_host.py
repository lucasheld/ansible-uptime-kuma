from uptime_kuma_api import DockerType

import plugins.modules.docker_host as module
from plugins.module_utils.common import get_docker_host_by_name
from .module_test_case import ModuleTestCase


class TestDockerHost(ModuleTestCase):
    def setUp(self):
        super(TestDockerHost, self).setUp()

        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None,
            "dockerType": None,
            "dockerDaemon": None,
            "state": "present"
        }

    def test_docker_host(self):
        # add docker host by name
        self.params.update({
            "name": "docker host 1",
            "dockerType": DockerType.SOCKET,
            "dockerDaemon": "/var/run/docker.sock",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        docker_host = get_docker_host_by_name(self.api, self.params["name"])
        self.assertEqual(docker_host["dockerType"], self.params["dockerType"])
        self.assertEqual(docker_host["dockerDaemon"], self.params["dockerDaemon"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # edit docker host by id
        docker_host_id = docker_host["id"]
        self.params.update({
            "id": docker_host_id,
            "dockerType": DockerType.TCP,
            "dockerDaemon": "tcp://localhost:2375",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
        docker_host = self.api.get_docker_host(docker_host_id)
        self.assertEqual(docker_host["dockerType"], self.params["dockerType"])
        self.assertEqual(docker_host["dockerDaemon"], self.params["dockerDaemon"])

        result = self.run_module(module, self.params)
        self.assertFalse(result["changed"])

        # delete docker host
        self.params.update({
            "state": "absent",
        })
        result = self.run_module(module, self.params)
        self.assertTrue(result["changed"])
