#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args, get_notification_by_name

import os, re
from uptimekumaapi import UptimeKumaApi, convert_from_socket, convert_to_socket, params_map_notification, params_map_notification_provider, notification_provider_options, NotificationType

__metaclass__ = type


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add notification
  lucasheld.uptime_kuma.notification:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Notification 1
    type: telegram
    isDefault: false
    telegramBotToken: 1111
    telegramChatID: 2222
    state: present

- name: Edit notification
  lucasheld.uptime_kuma.notification:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Notification 1
    type: telegram
    isDefault: false
    telegramBotToken: 6666
    telegramChatID: 7777
    state: present

- name: Remove notification
  lucasheld.uptime_kuma.notification:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Notification 1
    state: absent
'''

RETURN = r'''
'''


def build_provider_args(notification_provider_options):
    provider_args = {}
    for notification_provider_param in notification_provider_options:
        arg_data = {
            "type": str
        }
        if "password" in notification_provider_param.lower():
            arg_data["no_log"] = True
        provider_args[notification_provider_param] = arg_data
    
    provider_args = convert_from_socket(params_map_notification_provider, provider_args)
    return provider_args


def main():
    notification_provider_types = list(NotificationType.__dict__["_value2member_map_"].keys())
    notification_provider_options = list(params_map_notification_provider.keys())
    module_args = dict(
        name=dict(type="str", required=True),
        type=dict(type="str", choices=notification_provider_types),
        default=dict(type="bool", default=False),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    provider_args = build_provider_args(notification_provider_options)
    module_args.update(provider_args)
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    result = {}
    try:
        # type -> type_
        params["type_"] = params["type"]
        del params["type"]

        name = params["name"]
        state = params["state"]
        options = clear_params(params)
        # remove unset notification provider options
        options = {k: v for k, v in options.items() if v is not None and k not in notification_provider_options}

        notification = get_notification_by_name(api, name)

        changed = False
        failed_msg = None
        if state == "present":
            if not notification:
                r = api.add_notification(**options)
                if not r["ok"]:
                    failed_msg = r["msg"]
                changed = True
            else:
                notification = convert_from_socket(params_map_notification, notification)
                notification = convert_from_socket(params_map_notification_provider, notification)
                changed_keys = object_changed(notification, options)
                if changed_keys:
                    r = api.edit_notification(notification["id"], **options)
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
    
    except Exception as e:
        api.disconnect()
        module.fail_json(msg=str(e), **result)


if __name__ == '__main__':
    main()
