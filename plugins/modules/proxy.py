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

module: proxy
author: Lucas Held (@lucasheld)
short_description: Manages proxies.
description: Manages proxies.

options:
  id:
    description:
      - The id of the proxy.
      - Only required if no I(host), I(port) and I(protocol) specified.
    type: int
  host:
    description:
      - The host of the proxy.
      - Only required if no I(id) specified.
    type: str
    required: true
  port:
    description:
      - The port of the proxy.
      - Only required if no I(id) specified.
    type: int
    required: true
  protocol:
    description: The protocol of the proxy.
    type: str
  auth:
    description: True if the authentication is enabled.
    type: bool
  username:
    description: The username of the proxy.
    type: str
  password:
    description: The password of the proxy.
    type: str
  active:
    description: True if the proxy is active.
    type: bool
  default:
    description: True if the proxy is the default.
    type: bool
  applyExisting:
    description: True if the proxy is applied to existing monitors.
    type: bool
  state:
    description:
      - Set to C(present) to create/update a proxy.
      - Set to C(absent) to delete a proxy.
    type: str
    default: present
    choices: ["present", "absent"]
'''

EXAMPLES = r'''
- name: Add proxy
  lucasheld.uptime_kuma.proxy:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    protocol: http
    host: 127.0.0.1
    port: 8080
    state: present

- name: Edit proxy
  lucasheld.uptime_kuma.proxy:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    host: 127.0.0.1
    port: 8080
    active: false
    state: present

- name: Remove proxy
  lucasheld.uptime_kuma.proxy:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    host: 127.0.0.1
    port: 8080
    state: absent
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args, \
    get_proxy_by_host_port, clear_unset_params

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
        proxy = api.get_proxy(params["id"])
    else:
        proxy = get_proxy_by_host_port(api, params["host"], params["port"])

    if state == "present":
        if not proxy:
            api.add_proxy(**options)
            result["changed"] = True
        else:
            changed_keys = object_changed(proxy, options, {"applyExisting": [False, None]})
            if changed_keys:
                api.edit_proxy(proxy["id"], **options)
                result["changed"] = True
    elif state == "absent":
        if proxy:
            api.delete_proxy(proxy["id"])
            result["changed"] = True


def main():
    module_args = dict(
        id=dict(type="int"),
        host=dict(type="str", required=True),
        port=dict(type="int", required=True),
        protocol=dict(type="str"),
        auth=dict(type="bool"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        active=dict(type="bool"),
        default=dict(type="bool"),
        applyExisting=dict(type="bool"),
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
