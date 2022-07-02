#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule

from uptimekumaapi import UptimeKumaApi

__metaclass__ = type


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''


def main():
    module_args = {
        "api_url": {
            "type": str,
            "required": True
        },
        "api_username": {
            "type": str,
            "required": True
        },
        "api_password": {
            "type": str,
            "required": True,
            "no_log": True
        }
    }
    module = AnsibleModule(module_args)
    params = module.params
    api_url = params["api_url"]
    api_username = params["api_username"]
    api_password = params["api_password"]

    api = UptimeKumaApi(api_url)
    api.login(api_username, api_password)

    data = api.info()
    api.disconnect()

    result = data
    result["changed"] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()
