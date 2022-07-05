#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args

from uptimekumaapi import UptimeKumaApi, convert_from_socket, params_map_monitor

__metaclass__ = type


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add monitor
  lucasheld.uptime_kuma.monitor:
    type: keyword
    name: Peer 1
    url: http://192.168.20.135
    keyword: healthy
    state: present

- name: Edit monitor
  lucasheld.uptime_kuma.monitor:
    type: http
    name: Peer 1
    url: http://192.168.20.135
    state: present

- name: Remove monitor
  lucasheld.uptime_kuma.monitor:
    name: Peer 1
    state: absent

- name: Pause monitor
  lucasheld.uptime_kuma.monitor:
    name: Peer 1
    state: paused

- name: Resume monitor
  lucasheld.uptime_kuma.monitor:
    name: Peer 1
    state: resumed
'''

RETURN = r'''
'''


def get_monitor_by_name(api, name):
    monitors = api.get_monitors()
    for monitor in monitors:
        if monitor["name"] == name:
            return monitor


def main():
    module_args = {
        # general
        "name": {
            "type": str,
            "required": True
        },
        "type_": {
            "type": str,
            "choices": [
                "http",
                "port",
                "ping",
                "keyword",
                "dns",
                "push",
                "steam",
                "mqtt",
                "sqlserver"
            ]
        },
        "heartbeat_interval": {
            "type": int,
            "default": 60
        },
        "heartbeat_retry_interval": {
            "type": int,
            "default": 60
        },
        "retries": {
            "type": int,
            "default": 0
        },
        "upside_down_mode": {
            "type": bool,
            "default": False
        },
        # "tags": {
        #     "type": list[dict]
        # },
        "notification_ids": {
            "type": list[int],
            "default": None
        },

        # HTTP, KEYWORD
        "url": {
            "type": str,
            "default": None
        },
        "certificate_expiry_notification": {
            "type": bool,
            "default": False
        },
        "ignore_tls_error": {
            "type": bool,
            "default": False
        },
        "max_redirects": {
            "type": int,
            "default": 10
        },
        "accepted_status_codes": {
            "type": list[str],
            "default": None
        },
        "proxy_id": {
            "type": int,
            "default": None
        },
        "http_method": {
            "type": str,
            "default": "GET"
        },
        "http_body": {
            "type": str,
            "default": None
        },
        "http_headers": {
            "type": str,
            "default": None
        },
        "auth_method": {
            "type": str,
            "default": "",
            "choices": [
                "",
                "basic",
                "ntlm"
            ]
        },
        "auth_user": {
            "type": str,
            "default": None
        },
        "auth_pass": {
            "type": str,
            "default": None,
            "no_log": True
        },
        "auth_domain": {
            "type": str,
            "default": None
        },
        "auth_workstation": {
            "type": str,
            "default": None
        },

        # KEYWORD
        "keyword": {
            "type": str,
            "default": None
        },

        # DNS, PING, STEAM, MQTT
        "hostname": {
            "type": str,
            "default": None
        },

        # DNS, STEAM, MQTT
        "port": {
            "type": int,
            "default": 53
        },

        # DNS
        "dns_resolve_server": {
            "type": str,
            "default": "1.1.1.1"
        },
        "dns_resolve_type": {
            "type": str,
            "default": "A"
        },

        # MQTT
        "mqtt_username": {
            "type": str,
            "default": None
        },
        "mqtt_password": {
            "type": str,
            "default": None,
            "no_log": True
        },
        "mqtt_topic": {
            "type": str,
            "default": None
        },
        "mqtt_success_message": {
            "type": str,
            "default": None
        },

        # SQLSERVER
        "sqlserver_connection_string": {
            "type": str,
            "default": "Server=<hostname>,<port>;Database=<your database>;User Id=<your user id>;Password=<your password>;Encrypt=<true/false>;TrustServerCertificate=<Yes/No>;Connection Timeout=<int>"
        },
        "sqlserver_query": {
            "type": str,
            "default": None
        },

        "state": {
            "default": "present",
            "choices": [
                "present",
                "absent",
                "paused",
                "resumed"
            ]
        }
    }
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    if not params["accepted_status_codes"]:
        params["accepted_status_codes"] = ["200-299"]
    
    dict_notification_ids = {}
    if params["notification_ids"]:
        for notification_id in params["notification_ids"]:
            dict_notification_ids[notification_id] = True
    params["notification_ids"] = dict_notification_ids

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    state = params["state"]
    options = clear_params(params)

    monitor = get_monitor_by_name(api, params["name"])

    changed = False
    failed_msg = None
    result = {}
    if state == "present":
        if not monitor:
            r = api.add_monitor(**options)
            if not r["ok"]:
                failed_msg = r["msg"]
            changed = True
        else:
            monitor = convert_from_socket(params_map_monitor, monitor)
            changed_keys = object_changed(monitor, options)
            if changed_keys:
                r = api.edit_monitor(monitor["id"], **options)
                if not r["ok"]:
                    failed_msg = r["msg"]
                changed = True
    elif state == "absent":
        if monitor:
            r = api.delete_monitor(monitor["id"])
            if not r["ok"]:
                failed_msg = r["msg"]
            changed = True
    elif state == "paused":
        if monitor and monitor["active"] == 1:
            r = api.pause_monitor(monitor["id"])
            if not r["ok"]:
                failed_msg = r["msg"]
            changed = True
    elif state == "resumed":
        if monitor and monitor["active"] == 0:
            r = api.resume_monitor(monitor["id"])
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
