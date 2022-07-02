#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule

from uptimekumaapi import UptimeKumaApi

__metaclass__ = type


# TODO:
# notification edit


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add notification
  uptime_kuma_notification:
    name: Notification 1
    type: telegram
    isDefault: false
    telegramBotToken: 1111
    telegramChatID: 2222
    state: present
- name: Remove notification
  uptime_kuma_notification:
    name: Notification 1
    state: absent
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
        },
        "name": {
            "type": str,
            "required": True
        },
        "type": {
            "type": str
        },
        "isDefault": {
            "type": str
        },
        "telegramBotToken": {
            "type": str
        },
        "telegramChatID": {
            "type": str
        },
        "state": {
            "default": "present",
            "choices": [
                "present",
                "absent"
            ]
        }
    }
    module = AnsibleModule(module_args)
    params = module.params

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    name = params["name"]
    type_ = params["type"]
    is_default = params["isDefault"]
    state = params["state"]

    options = {k: v for k, v in params.items() if k not in [
        "api_url", "api_username", "api_password", "name", "type", "isDefault", "state"
    ]}

    notification = get_notification_by_name(api, name)

    changed = False
    failed_msg = False
    result = {}
    if state == "present":
        if not notification:
            r = api.add_notification(name, type_, is_default, **options)
            if not r["ok"]:
                failed_msg = r["msg"]
            changed = True
    elif state == "absent":
        if notification:
            r = api.delete_notification(notification["id"])
            if not r["ok"]:
                failed_msg = r["msg"]
            changed = True
    api.disconnect()

    if failed_msg:
        module.fail_json(msg=failed_msg, **result)

    result["changed"] = changed
    module.exit_json(**result)


if __name__ == '__main__':
    main()
