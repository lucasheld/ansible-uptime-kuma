#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
extends_documentation_fragment:
  - lucasheld.uptime_kuma.uptime_kuma

module: proxy_info
author: Lucas Held (@lucasheld)
short_description: Retrieves facts about proxies.
description: Retrieves facts about proxies.

options:
  id:
    description:
      - The id of the proxy to inspect.
      - Only required if no I(host) and I(port) specified.
    type: int
  host:
    description:
      - The host of the proxy to inspect.
      - Only required if no I(id) specified.
      - Only valid in combination with I(port).
    type: str
  port:
    description:
      - The port of the proxy to inspect.
      - Only required if no I(id) specified.
      - Only valid in combination with I(host).
    type: int
'''

EXAMPLES = r'''
- name: get all proxies
  lucasheld.uptime_kuma.proxy_info:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result
'''

RETURN = r'''
proxies:
  description: The proxies as list
  returned: always
  type: complex
  contains:
    id:
      description: The id of the proxy.
      returned: always
      type: int
      sample: 4
    userId:
      description: The user id of the proxy.
      returned: always
      type: int
      sample: 1
    protocol:
      description: The protocol of the proxy.
      returned: always
      type: str
      sample: http
    host:
      description: The host of the proxy.
      returned: always
      type: str
      sample: 127.0.0.1
    port:
      description: The port of the proxy.
      returned: always
      type: int
      sample: 8080
    auth:
      description: True if authentication is enabled.
      returned: always
      type: bool
      sample: False
    username:
      description: The authentication username of the proxy.
      returned: always
      type: str
      sample: None
    password:
      description: The authentication password of the proxy.
      returned: always
      type: str
      sample: None
    active:
      description: True if the proxy is active.
      returned: always
      type: bool
      sample: True
    default:
      description: True if the proxy is the default.
      returned: always
      type: bool
      sample: False
    createdDate:
      description: The creation date of the proxy.
      returned: always
      type: str
      sample: 2022-08-03 12:43:21
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_proxy_by_host_port
from ansible.module_utils.basic import missing_required_lib

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    if params["id"]:
        proxy = api.get_proxy(params["id"])
        result["proxies"] = [proxy]
    elif params["host"] and params["port"]:
        proxy = get_proxy_by_host_port(api, params["host"], params["port"])
        result["proxies"] = [proxy]
    else:
        result["proxies"] = api.get_proxies()


def main():
    module_args = dict(
        id=dict(type="int"),
        host=dict(type="str"),
        port=dict(type="int"),
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args, supports_check_mode=True)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
    api_token = params.get("api_token")
    api_username = params.get("api_username")
    api_password = params.get("api_password")
    if api_token:
        api.login_by_token(api_token)
    elif api_username and api_password:
        api.login(api_username, api_password)
    else:
        # autoLogin for enabled disableAuth
        api.login()

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
