#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args, get_proxy_by_protocol_host_port, get_notification_by_name, get_monitor_by_name

import traceback

from uptime_kuma_api import UptimeKumaApi

__metaclass__ = type


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    type: keyword
    name: Peer 1
    url: http://192.168.20.135
    keyword: healthy
    state: present

- name: Edit monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    type: http
    name: Peer 1
    url: http://192.168.20.135
    state: present

- name: Remove monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Peer 1
    state: absent

- name: Pause monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Peer 1
    state: paused

- name: Resume monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Peer 1
    state: resumed
'''

RETURN = r'''
'''


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
        proxy = get_proxy_by_protocol_host_port(api, params["proxy"]["protocol"], params["proxy"]["host"], params["proxy"]["port"])
        params["proxy_id"] = proxy["id"]
    else:
        params["proxy_id"] = params["proxy"]
    del params["proxy"]

    state = params["state"]
    options = clear_params(params)

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
        name=dict(type="str", required=True),
        type=dict(type="str", choices=["http", "port", "ping", "keyword", "dns", "push", "steam", "mqtt", "sqlserver"]),
        heartbeat_interval=dict(type="int", default=60),
        heartbeat_retry_interval=dict(type="int", default=60),
        retries=dict(type="int", default=0),
        upside_down_mode=dict(type="bool", default=False),
        # tags=dict(type="list", elements="dict", options=dict()),
        # notification_ids=dict(type="list", default=None, elements="int"),
        notifications=dict(type="list", default=None, elements="str"),

        # HTTP, KEYWORD
        url=dict(type="str", default=None),
        certificate_expiry_notification=dict(type="bool", default=False),
        ignore_tls_error=dict(type="bool", default=False),
        max_redirects=dict(type="int", default=10),
        accepted_status_codes=dict(type="list", default=None, elements="str"),
        # proxy_id=dict(type="int", default=None),
        proxy=dict(type="dict", default=None, options=dict(
            protocol=dict(type="str", required=True),
            host=dict(type="str", required=True),
            port=dict(type="int", required=True)
        )),
        http_method=dict(type="str", default="GET"),
        http_body=dict(type="str", default=None),
        http_headers=dict(type="str", default=None),
        auth_method=dict(type="str", default="", choices=["", "basic", "ntlm"]),
        auth_user=dict(type="str", default=None),
        auth_pass=dict(type="str", default=None, no_log=True),
        auth_domain=dict(type="str", default=None),
        auth_workstation=dict(type="str", default=None),

        # KEYWORD
        keyword=dict(type="str", default=None),

        # DNS, PING, STEAM, MQTT
        hostname=dict(type="str", default=None),

        # DNS, STEAM, MQTT
        port=dict(type="int", default=53),

        # DNS
        dns_resolve_server=dict(type="str", default="1.1.1.1"),
        dns_resolve_type=dict(type="str", default="A"),

        # MQTT
        mqtt_username=dict(type="str", default=None),
        mqtt_password=dict(type="str", default=None, no_log=True),
        mqtt_topic=dict(type="str", default=None),
        mqtt_success_message=dict(type="str", default=None),

        # SQLSERVER
        sqlserver_connection_string=dict(type="str", default="Server=<hostname>,<port>;Database=<your database>;User Id=<your user id>;Password=<your password>;Encrypt=<true/false>;TrustServerCertificate=<Yes/No>;Connection Timeout=<int>"),
        sqlserver_query=dict(type="str", default=None),

        state=dict(type="str", default="present", choices=["present", "absent", "paused", "resumed"])
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

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
