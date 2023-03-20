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

module: api_key_info
author: Lucas Held (@lucasheld)
short_description: Retrieves facts about api keys.
description: Retrieves facts about api keys.

options:
  id:
    description:
      - The id of the api key to inspect.
      - Only required if no I(name) specified.
    type: int
  name:
    description:
      - The name of the api key to inspect.
      - Only required if no I(id) specified.
    type: str
'''

EXAMPLES = r'''
- name: get all api keys
  lucasheld.uptime_kuma.api_key_info:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result
'''

RETURN = r'''
api_keys:
  description: The api keys as list
  returned: always
  type: complex
  contains:
    id:
      description: The id of the api key.
      returned: always
      type: int
      sample: 1
    name:
      description: The name of the api key.
      returned: always
      type: str
      sample: api key 1
    userID:
      description: The user id of the api key.
      returned: always
      type: int
      sample: 1
    createdDate:
      description: The creation date of the api key.
      returned: always
      type: str
      sample: "2023-03-20 11:15:05"
    active:
      description: True if the api key is active.
      returned: always
      type: bool
      sample: false
    expires:
      description: The expiration date of the api key.
      returned: always
      type: str
      sample: "2023-03-30 12:20:00"
    status:
      description: The status of the api key.
      returned: always
      type: str
      sample: "inactive"
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_api_key_by_name
from ansible.module_utils.basic import missing_required_lib

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    if params["id"]:
        api_key = api.get_api_key(params["id"])
        result["api_keys"] = [api_key]
    elif params["name"]:
        api_key = get_api_key_by_name(api, params["name"])
        result["api_keys"] = [api_key]
    else:
        result["api_keys"] = api.get_api_keys()


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
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
