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

module: api_key
author: Lucas Held (@lucasheld)
short_description: Manages api keys.
description: Manages api keys.

options:
  id:
    description:
      - The id of the api key.
      - Only required if no I(name) specified.
    type: int
  name:
    description:
      - The name of the api key.
      - Only required if no I(id) specified.
    type: str
  expires:
    description: The expiration date of the api key.
    type: str
  active:
    description: True to activate the api key.
    type: bool
  state:
    description:
      - Set to C(present) to create an api key.
      - Set to C(absent) to delete an api key.
      - Set to C(enabled) to enable an api key.
      - Set to C(disabled) to disable an api key.
    type: str
    default: present
    choices: ["present", "absent", "enabled", "disabled"]
'''

EXAMPLES = r'''
- name: Add api key
  lucasheld.uptime_kuma.api_key:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: api key 1
    expires: "2023-03-30 12:20:00"
    active: true
  register: result
- name: Extract the api key from the result and set it as fact
  set_fact:
    api_key: "{{ result.key }}"

- name: Enable api key
  lucasheld.uptime_kuma.api_key:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: api key 1
    state: enabled

- name: Disable api key
  lucasheld.uptime_kuma.api_key:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: api key 1
    state: disabled

- name: Remove api key
  lucasheld.uptime_kuma.api_key:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: api key 1
    state: absent
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args,\
    get_api_key_by_name, clear_params, clear_unset_params, object_changed

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
        api_key = api.get_api_key(params["id"])
    else:
        api_key = get_api_key_by_name(api, params["name"])

    if state == "present":
        if not api_key:
            r = api.add_api_key(**options)
            result["key"] = r["key"]
            result["changed"] = True
    elif state == "absent":
        if api_key:
            api.delete_api_key(api_key["id"])
            result["changed"] = True
    elif state == "enabled":
        if api_key and not api_key["active"]:
            api.enable_api_key(api_key["id"])
            result["changed"] = True
    elif state == "disabled":
        if api_key and api_key["active"]:
            api.disable_api_key(api_key["id"])
            result["changed"] = True

def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
        expires=dict(type="str"),
        active=dict(type="bool"),
        state=dict(type="str", default="present", choices=["present", "absent", "enabled", "disabled"])
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
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
