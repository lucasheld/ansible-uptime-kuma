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

module: monitor_tag
author: Lucas Held (@lucasheld)
short_description: Manages monitor tags.
description: Manages monitor tags.

options:
  monitor_id:
    description:
      - The id of the monitor to which the tag should be assigned.
      - Only required if no I(monitor_name) specified.
    type: int
  monitor_name:
    description:
      - The name of the monitor to which the tag should be assigned.
      - Only required if no I(monitor_id) specified.
    type: str
  tag_id:
    description:
      - The id of the tag that should be assigned.
      - Only required if no I(tag_name) specified.
    type: int
  tag_name:
    description:
      - The name of the tag that should be assigned.
      - Only required if no I(tag_id) specified.
    type: str
  value:
    description: The value that should be assigned.
    type: str
  state:
    description:
      - Set to C(present) to create a monitor tag.
      - Set to C(absent) to delete a monitor tag.
    type: str
    default: present
    choices: ["present", "absent"]
'''

EXAMPLES = r'''
- name: Add a monitor tag
  lucasheld.uptime_kuma.monitor_tag:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    monitor_name: Monitor 1
    tag_name: Tag 1
    value: Tag value
    state: present

- name: Remove a monitor tag
  lucasheld.uptime_kuma.monitor_tag:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    monitor_name: Monitor 1
    tag_name: Tag 1
    value: Tag Value
    state: absent
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_monitor_by_name, get_tag_by_name, get_monitor_tag

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    value = params["value"]
    if not value:
        value = ""

    state = params["state"]

    monitor_id = params["monitor_id"]
    tag_id = params["tag_id"]
    if monitor_id and tag_id:
        monitor = api.get_monitor(monitor_id)
        tag = api.get_tag(tag_id)
    else:
        monitor = get_monitor_by_name(api, params["monitor_name"])
        tag = get_tag_by_name(api, params["tag_name"])
        tag_id = tag["id"]
        monitor_id = monitor["id"]

    monitor_tag = get_monitor_tag(monitor, tag, value)

    if state == "present":
        if not monitor_tag:
            api.add_monitor_tag(tag_id, monitor_id, value)
            result["changed"] = True
    elif state == "absent":
        if monitor_tag:
            api.delete_monitor_tag(tag_id, monitor_id, value)
            result["changed"] = True


def main():
    module_args = dict(
        monitor_id=dict(type="int"),
        tag_id=dict(type="int"),
        monitor_name=dict(type="str"),
        tag_name=dict(type="str"),
        value=dict(type="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"], timeout=params["api_timeout"], headers=params["api_headers"], ssl_verify=params["api_ssl_verify"], wait_events=params["api_wait_events"])
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
