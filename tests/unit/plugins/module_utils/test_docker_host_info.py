from packaging.version import parse as parse_version

import plugins.modules.docker_host_info as module
from .module_test_case import ModuleTestCase


class TestDockerHostInfo(ModuleTestCase):
    def setUp(self):
        super(TestDockerHostInfo, self).setUp()

        if parse_version(self.api.version) < parse_version("1.18"):
            super(TestDockerHostInfo, self).tearDown()
            self.skipTest("Unsupported in this Uptime Kuma version")

        self.params = {
            "api_url": "http://127.0.0.1:3001",
            "api_username": None,
            "api_password": None,
            "api_token": None,
            "id": None,
            "name": None
        }
        self.docker_host_id_1 = self.add_docker_host("docker host 1")
        self.docker_host_id_2 = self.add_docker_host("docker host 2")

    def test_all_docker_hosts(self):
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        docker_host_ids = [self.docker_host_id_1, self.docker_host_id_2]
        self.assertEqual(len(result["docker_hosts"]), len(docker_host_ids))
        self.assertEqual([i["id"] for i in result["docker_hosts"]], docker_host_ids)

    def test_docker_host_by_id(self):
        self.params["id"] = self.docker_host_id_2
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["docker_hosts"]), 1)
        self.assertEqual(result["docker_hosts"][0]["id"], self.docker_host_id_2)

    def test_docker_host_by_name(self):
        name = "docker host 2"
        self.params["name"] = name
        result = self.run_module(module, self.params)

        self.assertFalse(result["changed"])
        self.assertEqual(len(result["docker_hosts"]), 1)
        self.assertEqual(result["docker_hosts"][0]["name"], name)
