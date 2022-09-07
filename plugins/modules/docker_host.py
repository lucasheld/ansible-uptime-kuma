#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
extends_documentation_fragment:
  - lucasheld.uptime_kuma.uptime_kuma

module: docker_host
author: Lucas Held (@lucasheld)
short_description: Manages docker hosts.
description: Manages docker hosts.

options:
  id:
    description:
      - The id of the docker host.
      - Only required if no I(name) specified.
    type: int
  name:
    description:
      - The name of the docker host.
      - Only required if no I(id) specified.
    type: str
  dockerType:
    description: The docker type of the docker host.
    type: str
    choices: ["socket", "tcp"]
  dockerDaemon:
    description: The docker daemon of the docker host.
    type: str
  state:
    description:
      - Set to C(present) to create a docker host.
      - Set to C(absent) to delete a docker host.
    type: str
    default: present
    choices: ["present", "absent"]
'''

EXAMPLES = r'''
- name: Add docker host
  lucasheld.uptime_kuma.docker_host:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Docker host 1
    dockerType: socket
    dockerDaemon: /var/run/docker.sock

- name: Remove docker host
  lucasheld.uptime_kuma.docker_host:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Docker host 1
    state: absent
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args,\
    get_docker_host_by_name, clear_params, clear_unset_params, object_changed

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    state = params["state"]
    options = clear_params(params)
    options = clear_unset_params(options)

    if params["id"]:
        docker_host = api.get_docker_host(params["id"])
    else:
        docker_host = get_docker_host_by_name(api, params["name"])

    if state == "present":
        if not docker_host:
            api.add_docker_host(**options)
            result["changed"] = True
        else:
            changed_keys = object_changed(docker_host, options)
            if changed_keys:
                api.edit_docker_host(docker_host["id"], **options)
                result["changed"] = True
    elif state == "absent":
        if docker_host:
            api.delete_docker_host(docker_host["id"])
            result["changed"] = True


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
        dockerType=dict(type="str"),
        dockerDaemon=dict(type="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
    api_token = params.get("api_token")
    if api_token:
      api.login_by_token(api_token)
    else:
      api.login(params["api_username"], params["api_password"])

    result = {
        "changed": False
    }

    try:
        run(api, params, result)

        api.disconnect()
        module.exit_json(**result)
    except Exception:
        api.disconnect()
        error = traceback.format_exc()
        module.fail_json(msg=error, **result)


if __name__ == '__main__':
    main()
