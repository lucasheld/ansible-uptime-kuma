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

module: notification
version_added: 0.0.0
author: Lucas Held (@lucasheld)
short_description: Return information about the Uptime Kuma instance
description: Return information about the Uptime Kuma instance

options:
  name:
    description: TODO
    type: str
    required: true
  default:
    description: TODO
    type: bool
    default: false
  state:
    description: TODO
    type: str
    default: present
    choices: ["present", "absent"]
'''

EXAMPLES = r'''
- name: Add notification
  lucasheld.uptime_kuma.notification:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Notification 1
    type: telegram
    default: false
    telegram_bot_token: 1111
    telegram_chat_id: 2222
    state: present

- name: Edit notification
  lucasheld.uptime_kuma.notification:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Notification 1
    type: telegram
    default: false
    telegram_bot_token: 6666
    telegram_chat_id: 7777
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

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args, get_notification_by_name

try:
    from uptime_kuma_api import UptimeKumaApi, params_map_notification_provider, NotificationType

    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def build_provider_args():
    provider_args = {}
    for notification_provider_param in notification_provider_options:
        arg_data = dict(type="str")
        if "password" in notification_provider_param.lower():
            arg_data["no_log"] = True
        provider_args[notification_provider_param] = arg_data
    return provider_args


def run(api, params, result):
    # type -> type_
    params["type_"] = params.pop("type")

    name = params["name"]
    state = params["state"]
    options = clear_params(params)
    # remove unset notification provider options
    options = {k: v for k, v in options.items() if not (k in notification_provider_options and v is None)}

    notification = get_notification_by_name(api, name)

    if state == "present":
        if not notification:
            api.add_notification(**options)
            result["changed"] = True
        else:
            changed_keys = object_changed(notification, options)
            if changed_keys:
                api.edit_notification(notification["id"], **options)
                result["changed"] = True
    elif state == "absent":
        if notification:
            api.delete_notification(notification["id"])
            result["changed"] = True


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        default=dict(type="bool", default=False),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )

    if HAS_UPTIME_KUMA_API:
        global notification_provider_types
        global notification_provider_options
        notification_provider_types = list(NotificationType.__dict__["_value2member_map_"].keys())
        notification_provider_options = list(params_map_notification_provider.values())

        module_args.update(type=dict(type="str", choices=notification_provider_types))
        provider_args = build_provider_args()
        module_args.update(provider_args)

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
    notification_provider_types = None
    notification_provider_options = None
    main()
