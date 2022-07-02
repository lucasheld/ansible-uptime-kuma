#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule

from uptimekumaapi import UptimeKumaApi

__metaclass__ = type


# TODO:
# monitor edit


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add monitor
  uptime_kuma_monitor:
    monitor_type: keyword
    friendly_name: Peer 1
    url: http://192.168.20.135
    keyword: healthy
    state: present
- name: Remove monitor
  uptime_kuma_monitor:
    friendly_name: Peer 1
    state: absent
- name: Pause monitor
  uptime_kuma_monitor:
    friendly_name: Peer 1
    state: paused
- name: Resume monitor
  uptime_kuma_monitor:
    friendly_name: Peer 1
    state: resumed
'''

RETURN = r'''
'''


def get_monitor_by_name(api, name):
    monitors = api.get_monitors()
    for monitor in monitors.values():
        if monitor["name"] == name:
            return monitor


def main():
    """
    >>> import uptimekumaapi
    >>> import inspect
    >>> inspect.signature(uptimekumaapi.UptimeKumaApi("http://192.168.20.160:3001/")._build_monitor_data)
    <Signature (monitor_type: uptimekumaapi.monitor_type.MonitorType, friendly_name: str, heartbeat_interval: int = 60, heartbeat_retry_interval: int = 60, retries: int = 0, upside_down_mode: bool = False, tags: list = None, notification_ids: list[int] = None, url: str = None, certificate_expiry_notification: bool = False, ignore_tls_error: bool = False, max_redirects: int = 10, accepted_status_codes: list[str] = None, proxy_id: int = None, http_method: str = 'GET', http_body: str = None, http_headers: str = None, auth_method: uptimekumaapi.auth_method.AuthMethod = <AuthMethod.NONE: ''>, auth_user: str = None, auth_pass: str = None, auth_domain: str = None, auth_workstation: str = None, keyword: str = None, hostname: str = None, port: int = 53, dns_resolve_server: str = '1.1.1.1', dns_resolve_type: str = 'A', mqtt_username: str = None, mqtt_password: str = None, mqtt_topic: str = None, mqtt_success_message: str = None, sqlserver_connection_string: str = 'Server=<hostname>,<port>;Database=<your database>;User Id=<your user id>;Password=<your password>;Encrypt=<true/false>;TrustServerCertificate=<Yes/No>;Connection Timeout=<int>', sqlserver_query: str = None)>
    """

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
        "friendly_name": {
            "type": str,
            "required": True
        },
        "monitor_type": {
            "type": str
        },
        "url": {
            "type": str
        },
        "keyword": {
            "type": str
        },
        "state": {
            "default": "present",
            "choices": [
                "present",
                "absent",
                "paused",
                "resumed",
            ]
        }
    }
    module = AnsibleModule(module_args)
    params = module.params

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    options = {k: v for k, v in params.items() if k not in [
        "api_url", "api_username", "api_password", "state"
    ]}

    name = options["friendly_name"]
    state = params["state"]

    changed = False
    result = {}
    if state == "present":
        monitor = get_monitor_by_name(api, name)
        if not monitor:
            result = api.add_monitor(**options)
            changed = True
    elif state == "absent":
        monitor = get_monitor_by_name(api, name)
        if monitor:
            result = api.delete_monitor(monitor["id"])
            changed = True
    elif state == "paused":
        monitor = get_monitor_by_name(api, name)
        if monitor and monitor["active"] == 1:
            result = api.pause_monitor(monitor["id"])
            changed = True
    elif state == "resumed":
        monitor = get_monitor_by_name(api, name)
        if monitor and monitor["active"] == 0:
            result = api.resume_monitor(monitor["id"])
            changed = True
    api.disconnect()

    if result and not result['ok']:
        module.fail_json(msg=result["msg"], **result)

    result["changed"] = changed
    module.exit_json(**result)


if __name__ == '__main__':
    main()
