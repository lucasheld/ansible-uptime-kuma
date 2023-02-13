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

module: tag
author: Lucas Held (@lucasheld)
short_description: Manages tags.
description: Manages tags.

options:
  id:
    description:
      - The id of the tag.
      - Only required if no I(name) specified.
    type: int
  name:
    description:
      - The name of the tag.
      - Only required if no I(id) specified.
    type: str
  color:
    description: The color of the tag.
    type: str
  state:
    description:
      - Set to C(present) to create a tag.
      - Set to C(absent) to delete a tag.
    type: str
    default: present
    choices: ["present", "absent"]
'''

EXAMPLES = r'''
- name: Add tag
  lucasheld.uptime_kuma.tag:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Tag 1
    color: "#ff0000"
    state: present

- name: Edit tag
  lucasheld.uptime_kuma.tag:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Tag 1
    color: "#ffffff"
    state: present

- name: Remove tag
  lucasheld.uptime_kuma.tag:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Tag 1
    state: absent
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_tag_by_name, \
    clear_params, object_changed, clear_unset_params

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
        tag = api.get_tag(params["id"])
    else:
        tag = get_tag_by_name(api, params["name"])

    if state == "present":
        if not tag:
            api.add_tag(**options)
            result["changed"] = True
        else:
            changed_keys = object_changed(tag, options)
            if changed_keys:
                api.edit_tag(tag["id"], **options)
                result["changed"] = True
    elif state == "absent":
        if tag:
            api.delete_tag(tag["id"])
            result["changed"] = True


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
        color=dict(type="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
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
