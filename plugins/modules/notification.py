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
author: Lucas Held (@lucasheld)
short_description: Manages notifications.
description: Manages notifications.

options:
  id:
    description:
      - The id of the notification.
      - Only required if no I(name) specified.
    type: int
  name:
    description:
      - The name of the notification.
      - Only required if no I(id) specified.
    type: str
  isDefault:
    description: True if the notification is the default.
    type: bool
  applyExisting:
    description: True if the notification is applied to all existing monitors.
    type: bool
  state:
    description:
      - Set to C(present) to create/update a notification.
      - Set to C(absent) to delete a notification.
    type: str
    default: present
    choices: ["present", "absent"]
'''

EXAMPLES = r'''
- name: Add notification
  lucasheld.uptime_kuma.notification:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Notification 1
    type: telegram
    isDefault: false
    applyExisting: false
    telegramBotToken: 1111
    telegramChatID: 2222
    state: present

- name: Edit notification
  lucasheld.uptime_kuma.notification:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Notification 1
    type: telegram
    isDefault: false
    applyExisting: false
    telegramBotToken: 6666
    telegramChatID: 7777
    state: present

- name: Remove notification
  lucasheld.uptime_kuma.notification:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Notification 1
    state: absent
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args, get_notification_by_name, \
    clear_unset_params

try:
    from uptime_kuma_api import UptimeKumaApi, notification_provider_options

    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def build_provider_args():
    provider_args = {}
    for provider_options in notification_provider_options.values():
        if type(provider_options) == list:  # backward compatible
            provider_options = {option: dict(type="str") for option in provider_options}
        for option, args in provider_options.items():
            if "password" in option.lower():
                args["no_log"] = True
            provider_args[option] = args
    return provider_args


def build_providers():
    providers = []
    for provider_enum in notification_provider_options:
        provider = provider_enum.__dict__["_value_"]
        providers.append(provider)
    return providers


def build_provider_options():
    options = []
    for provider_options in notification_provider_options.values():
        options.extend(provider_options)
    return options


def run(api, params, result):
    state = params["state"]
    options = clear_params(params)
    options = clear_unset_params(options)

    if params["id"]:
        notification = api.get_notification(params["id"])
    else:
        notification = get_notification_by_name(api, params["name"])

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
        id=dict(type="int"),
        name=dict(type="str"),
        isDefault=dict(type="bool", aliases=["default"]),
        applyExisting=dict(type="bool"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )

    if HAS_UPTIME_KUMA_API:
        provider_types = build_providers()
        module_args.update(type=dict(type="str", choices=provider_types))

        provider_args = build_provider_args()
        module_args.update(provider_args)

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
