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
version_added: 0.0.0
author: Lucas Held (@lucasheld)
short_description: Manages monitors.
description: Manages monitors.

options:
  id:
    description: The id of the monitor.
    type: int
  name:
    description: The name of the monitor.
    type: str
  type:
    description: The type of the monitor.
    type: str
    choices: ["http", "port", "ping", "keyword", "dns", "push", "steam", "mqtt", "sqlserver"]
  heartbeat_interval:
    description: The heartbeat interval of the monitor.
    type: int
  heartbeat_retry_interval:
    description: The heartbeat retry interval of the monitor.
    type: int
  retries:
    description: The retries of the monitor.
    type: int
  upside_down_mode:
    description: True if upside down mode is enabled.
    type: bool
  notifications:
    description: The notification names of the monitor.
    type: list
    elements: str
  url:
    description: The url of the monitor.
    type: str
  certificate_expiry_notification:
    description: True if certificate expiry notification is enabled.
    type: bool
  ignore_tls_error:
    description: True if ignore tls error is enabled.
    type: bool
  max_redirects:
    description: The max redirects of the monitor.
    type: int
  accepted_status_codes:
    description: The accepted status codes of the monitor.
    type: list
    elements: str
  proxy:
    description: The proxy of the monitor.
    type: dict
    suboptions:
      host:
        description: The host of the proxy.
        type: str
        required: true
      port:
        description: The port of the proxy.
        type: int
        required: true
  http_method:
    description: The http method of the monitor.
    type: str
  http_body:
    description: The http body of the monitor.
    type: str
  http_headers:
    description: The http headers of the monitor.
    type: str
  auth_method:
    description: The auth method of the monitor.
    type: str
    choices: ["", "basic", "ntlm"]
  auth_user:
    description: The auth user of the monitor.
    type: str
  auth_pass:
    description: The auth pass of the monitor.
    type: str
  auth_domain:
    description: The auth domain of the monitor.
    type: str
  auth_workstation:
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
  mqtt_username:
    description: The mqtt username of the monitor.
    type: str
  mqtt_password:
    description: The mqtt password of the monitor.
    type: str
  mqtt_topic:
    description: The mqtt topic of the monitor.
    type: str
  mqtt_success_message:
    description: The mqtt success message of the monitor.
    type: str
  sqlserver_connection_string:
    description: The sqlserver connection string of the monitor.
    type: str
  sqlserver_query:
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
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    type: keyword
    name: Peer 1
    url: http://192.168.20.135
    keyword: healthy
    state: present

- name: Edit a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    type: http
    name: Peer 1
    url: http://192.168.20.135
    state: present

- name: Remove a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Peer 1
    state: absent

- name: Pause a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Peer 1
    state: paused

- name: Resume a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Peer 1
    state: resumed
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args, \
    get_proxy_by_host_port, get_notification_by_name, get_monitor_by_name, clear_unset_params

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    if not params["accepted_status_codes"]:
        params["accepted_status_codes"] = ["200-299"]

    # type -> type_
    params["type_"] = params.pop("type")

    # notifications -> notification_ids
    dict_notification_ids = {}
    if params["notifications"]:
        for notification_name in params["notifications"]:
            notification = get_notification_by_name(api, notification_name)
            notification_id = notification["id"]
            dict_notification_ids[notification_id] = True
    params["notification_ids"] = dict_notification_ids
    del params["notifications"]

    # proxy -> proxy_id
    if params["proxy"]:
        proxy = get_proxy_by_host_port(api, params["proxy"]["host"], params["proxy"]["port"])
        params["proxy_id"] = proxy["id"]
    else:
        params["proxy_id"] = params["proxy"]
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
        heartbeat_interval=dict(type="int"),
        heartbeat_retry_interval=dict(type="int"),
        retries=dict(type="int"),
        upside_down_mode=dict(type="bool"),
        # tags=dict(type="list", elements="dict", options=dict()),
        # notification_ids=dict(type="list", elements="int"),
        notifications=dict(type="list", elements="str"),

        # HTTP, KEYWORD
        url=dict(type="str"),
        certificate_expiry_notification=dict(type="bool"),
        ignore_tls_error=dict(type="bool"),
        max_redirects=dict(type="int"),
        accepted_status_codes=dict(type="list", elements="str"),
        # proxy_id=dict(type="int"),
        proxy=dict(type="dict", options=dict(
            host=dict(type="str", required=True),
            port=dict(type="int", required=True)
        )),
        http_method=dict(type="str"),
        http_body=dict(type="str"),
        http_headers=dict(type="str"),
        auth_method=dict(type="str", choices=["", "basic", "ntlm"]),
        auth_user=dict(type="str"),
        auth_pass=dict(type="str", no_log=True),
        auth_domain=dict(type="str"),
        auth_workstation=dict(type="str"),

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
        mqtt_username=dict(type="str"),
        mqtt_password=dict(type="str", no_log=True),
        mqtt_topic=dict(type="str"),
        mqtt_success_message=dict(type="str"),

        # SQLSERVER
        sqlserver_connection_string=dict(
            type="str",
        ),
        sqlserver_query=dict(type="str"),

        state=dict(type="str", default="present", choices=["present", "absent", "paused", "resumed"])
    )
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
    main()
