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

module: monitor
author: Lucas Held (@lucasheld)
short_description: Manages monitors.
description: Manages monitors.

options:
  id:
    description:
      - The id of the monitor.
      - Only required if no I(name) specified.
    type: int
  name:
    description:
      - The name of the monitor.
      - Only required if no I(id) specified.
    type: str
  type:
    description: The type of the monitor.
    type: str
    choices: ["http", "port", "ping", "keyword", "dns", "push", "steam", "mqtt", "sqlserver"]
  interval:
    description: The heartbeat interval of the monitor.
    type: int
  retryInterval:
    description: The heartbeat retry interval of the monitor.
    type: int
  maxretries:
    description: The max retries of the monitor.
    type: int
  upsideDown:
    description: True if upside down mode is enabled.
    type: bool
  notificationIDList:
    description:
      - The notification ids of the monitor.
      - Only required if I(notification_names) not specified.
    type: list
    elements: int
  notification_names:
    description:
      - The notification names of the monitor.
      - Only required if I(notificationIDList) not specified.
    type: list
    elements: str
  url:
    description: The url of the monitor.
    type: str
  expiryNotification:
    description: True if certificate expiry notification is enabled.
    type: bool
  ignoreTls:
    description: True if ignore tls error is enabled.
    type: bool
  maxredirects:
    description: The redirects of the monitor.
    type: int
  accepted_statuscodes:
    description: The accepted status codes of the monitor.
    type: list
    elements: str
  proxyId:
    description:
      - The proxy id of the monitor.
      - Only required if no I(proxy) specified.
    type: int
  proxy:
    description: The proxy of the monitor.
    type: dict
    suboptions:
      host:
        description:
          - The host of the proxy.
          - Only required if no I(proxyId) specified.
        type: str
      port:
        description:
          - The port of the proxy.
          - Only required if no I(proxyId) specified.
        type: int
  method:
    description: The http method of the monitor.
    type: str
  body:
    description: The http body of the monitor.
    type: str
  headers:
    description: The http headers of the monitor.
    type: str
  authMethod:
    description: The auth method of the monitor.
    type: str
    choices: ["", "basic", "ntlm"]
  basic_auth_user:
    description: The auth user of the monitor.
    type: str
  basic_auth_pass:
    description: The auth pass of the monitor.
    type: str
  authDomain:
    description: The auth domain of the monitor.
    type: str
  authWorkstation:
    description: The auth workstation of the monitor.
    type: str
  keyword:
    description: The keyword of the monitor.
    type: str
  hostname:
    description: The hostname of the monitor.
    type: str
  port:
    description: The port of the monitor.
    type: int
  dns_resolve_server:
    description: The dns resolve server of the monitor.
    type: str
  dns_resolve_type:
    description: The dns resolve type of the monitor.
    type: str
  mqttUsername:
    description: The mqtt username of the monitor.
    type: str
  mqttPassword:
    description: The mqtt password of the monitor.
    type: str
  mqttTopic:
    description: The mqtt topic of the monitor.
    type: str
  mqttSuccessMessage:
    description: The mqtt success message of the monitor.
    type: str
  databaseConnectionString:
    description: The sqlserver connection string of the monitor.
    type: str
  databaseQuery:
    description: The sqlserver query of the monitor.
    type: str
  state:
    description:
      - Set to C(present) to create/update a monitor.
      - Set to C(absent) to delete a monitor.
      - Set to C(paused) to pause a monitor.
      - Set to C(resumed) to resume a monitor.
    type: str
    default: present
    choices: ["present", "absent", "paused", "resumed"]
'''

EXAMPLES = r'''
- name: Add a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    type: keyword
    name: Monitor 1
    url: http://192.168.20.135
    keyword: healthy
    state: present

- name: Edit a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    type: http
    name: Monitor 1
    url: http://192.168.20.135
    state: present

- name: Remove a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Monitor 1
    state: absent

- name: Pause a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Monitor 1
    state: paused

- name: Resume a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Monitor 1
    state: resumed
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, \
    common_module_args, get_proxy_by_host_port, get_notification_by_name, get_monitor_by_name, clear_unset_params

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    if not params["accepted_statuscodes"]:
        params["accepted_statuscodes"] = ["200-299"]

    # notification_names -> notificationIDList
    if params["notification_names"]:
        notification_ids = []
        for notification_name in params["notification_names"]:
            notification = get_notification_by_name(api, notification_name)
            notification_ids.append(notification["id"])
        params["notificationIDList"] = notification_ids
    del params["notification_names"]

    # proxy -> proxyId
    if params["proxy"]:
        proxy = get_proxy_by_host_port(api, params["proxy_id"]["host"], params["proxy_id"]["port"])
        params["proxyId"] = proxy["id"]
    del params["proxy"]

    state = params["state"]
    options = clear_params(params)
    options = clear_unset_params(options)

    if params["id"]:
        monitor = api.get_monitor(params["id"])
    else:
        monitor = get_monitor_by_name(api, params["name"])

    if state == "present":
        if not monitor:
            api.add_monitor(**options)
            result["changed"] = True
        else:
            changed_keys = object_changed(monitor, options)
            if changed_keys:
                api.edit_monitor(monitor["id"], **options)
                result["changed"] = True
    elif state == "absent":
        if monitor:
            api.delete_monitor(monitor["id"])
            result["changed"] = True
    elif state == "paused":
        if monitor and monitor["active"]:
            api.pause_monitor(monitor["id"])
            result["changed"] = True
    elif state == "resumed":
        if monitor and not monitor["active"]:
            api.resume_monitor(monitor["id"])
            result["changed"] = True


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
        type=dict(type="str", choices=["http", "port", "ping", "keyword", "dns", "push", "steam", "mqtt", "sqlserver"]),
        interval=dict(type="int"),
        retryInterval=dict(type="int"),
        maxretries=dict(type="int"),
        upsideDown=dict(type="bool"),
        # tags=dict(type="list", elements="dict", options=dict()),
        notificationIDList=dict(type="list", elements="int"),
        notification_names=dict(type="list", elements="str"),

        # HTTP, KEYWORD
        url=dict(type="str"),
        expiryNotification=dict(type="bool"),
        ignoreTls=dict(type="bool"),
        maxredirects=dict(type="int"),
        accepted_statuscodes=dict(type="list", elements="str"),
        proxyId=dict(type="int"),
        proxy=dict(type="dict", options=dict(
            host=dict(type="str"),
            port=dict(type="int")
        )),
        method=dict(type="str"),
        body=dict(type="str"),
        headers=dict(type="str"),
        authMethod=dict(type="str", choices=["", "basic", "ntlm"]),
        basic_auth_user=dict(type="str"),
        basic_auth_pass=dict(type="str", no_log=True),
        authDomain=dict(type="str"),
        authWorkstation=dict(type="str"),

        # KEYWORD
        keyword=dict(type="str"),

        # DNS, PING, STEAM, MQTT
        hostname=dict(type="str"),

        # DNS, STEAM, MQTT
        port=dict(type="int"),

        # DNS
        dns_resolve_server=dict(type="str"),
        dns_resolve_type=dict(type="str"),

        # MQTT
        mqttUsername=dict(type="str"),
        mqttPassword=dict(type="str", no_log=True),
        mqttTopic=dict(type="str"),
        mqttSuccessMessage=dict(type="str"),

        # SQLSERVER
        databaseConnectionString=dict(type="str"),
        databaseQuery=dict(type="str"),

        state=dict(type="str", default="present", choices=["present", "absent", "paused", "resumed"])
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
    api_token = params.get("api_token")
    if api_token:
      api.login_by_token(api_token)
    else:
      api.login(params["api_username"], params["api_password"])

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
