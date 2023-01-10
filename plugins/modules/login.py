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

module: login
author: Lucas Held (@lucasheld)
short_description: Login to Uptime Kuma.
description: Login to Uptime Kuma and returns a token that can be used for future requests.

options:
  api_2fa:
    description:
      - The Uptime Kuma 2FA token.
      - Only required if no I(api_token) specified and authentication with 2FA is enabled.
'''

EXAMPLES = r'''
- name: login
  lucasheld.uptime_kuma.login:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123

- name: login with 2fa
  lucasheld.uptime_kuma.login:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    api_2fa: 123456
'''

RETURN = r'''
token:
  description: The login token.
  type: str
  returned: always
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    api_username = params["api_username"]
    api_password = params["api_password"]
    api_2fa = params["api_2fa"]

    r = api.login(api_username, api_password, api_2fa)
    result["token"] = r["token"]


def main():
    module_args = {}
    module_args.update(common_module_args)
    module_args.update({"api_2fa": dict(type="str", no_log=True)})

    module = AnsibleModule(module_args)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])

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
