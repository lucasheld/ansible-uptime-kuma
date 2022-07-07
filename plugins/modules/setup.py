#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args

import traceback

from uptime_kuma_api import UptimeKumaApi

__metaclass__ = type


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Setup
  lucasheld.uptime_kuma.setup:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
'''

RETURN = r'''
'''


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
    module_args = {}
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    api = UptimeKumaApi(params["api_url"])

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
