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

module: setup
author: Lucas Held (@lucasheld)
short_description: Setup the initial username and password.
description: Setup the initial username and password.
'''

EXAMPLES = r'''
- name: Setup
  lucasheld.uptime_kuma.setup:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
'''

RETURN = r'''
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

    need_setup = api.need_setup()
    if need_setup:
        api.setup(api_username, api_password)
        result["changed"] = True

    # check login
    api.login(api_username, api_password)


def main():
    module_args = dict()
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"], wait_timeout=params["api_wait_timeout"], headers=params["api_headers"])

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
