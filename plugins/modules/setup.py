#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule

from uptimekumaapi import UptimeKumaApi

__metaclass__ = type


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Setup
  lucasheld.uptime_kuma.setup:
    api_url: 
    api_username: 
    api_password: 
'''

RETURN = r'''
'''


def get_notification_by_name(api, name):
    notifications = api.get_notifications()
    for notification in notifications:
        if notification["name"] == name:
            return notification


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

    changed = False
    failed_msg = False
    result = {}
    need_setup = api.need_setup()
    if need_setup:
        api.setup(api_username, api_password)
        changed = True

    r = api.login(api_username, api_password)
    if not r["ok"]:
        failed_msg = r["msg"]

    api.disconnect()

    if failed_msg:
        module.fail_json(msg=failed_msg, **result)

    result["changed"] = changed
    module.exit_json(**result)


if __name__ == '__main__':
    main()
