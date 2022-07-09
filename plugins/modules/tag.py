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

module: tag
version_added: 0.0.0
author: Lucas Held (@lucasheld)
short_description: Return information about the Uptime Kuma instance
description: Return information about the Uptime Kuma instance

options:
  name:
    description: TODO
    type: str
    required: true
  color:
    description: TODO
    type: str
  state:
    description: TODO
    type: str
    default: "present"
    choices: ["present", "absent"]
'''

EXAMPLES = r'''
- name: Add tag
  uptime_kuma_tag:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Tag 1
    color: "#ff0000"
    state: present

- name: Remove tag
  uptime_kuma_tag:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Tag 1
    state: absent
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_tag_by_name

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    name = params["name"]
    color = params["color"]
    state = params["state"]

    tag = get_tag_by_name(api, name)

    if state == "present":
        if not tag:
            api.add_tag(name, color)
            result["changed"] = True
    elif state == "absent":
        if tag:
            api.delete_tag(tag["id"])
            result["changed"] = True


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        color=dict(type="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    result = {
        "changed": False
    }

    try:
        run(api, params, result)

        api.disconnect()
        module.exit_json(**result)
    except Exception as e:
        api.disconnect()
        error = traceback.format_exc()
        module.fail_json(msg=error, **result)


if __name__ == '__main__':
    main()
