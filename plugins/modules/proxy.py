#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args

from uptimekumaapi import UptimeKumaApi, convert_from_socket, params_map_proxy

__metaclass__ = type


# TODO:
# add more options


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add proxy
  lucasheld.uptime_kuma.proxy:
    protocol: http
    host: 127.0.0.1
    port: 8080
    state: present

- name: Edit proxy
  lucasheld.uptime_kuma.proxy:
    protocol: https
    host: 127.0.0.1
    port: 8080
    state: present

- name: Remove proxy
  lucasheld.uptime_kuma.proxy:
    protocol: http
    host: 127.0.0.1
    port: 8080
    state: absent
'''

RETURN = r'''
'''


def get_proxy_by_protocol_host_port(api, protocol, host, port):
    proxies = api.get_proxies()
    for proxy in proxies:
        if proxy["protocol"] == protocol and proxy["host"] == host and proxy["port"] == port:
            return proxy


def main():
    module_args = {
        "protocol": {
            "type": str,
            "required": True
        },
        "host": {
            "type": str,
            "required": True
        },
        "port": {
            "type": int,
            "required": True
        },
        "auth": {
            "type": bool,
            "default": False
        },
        "username": {
            "type": str,
            "default": None
        },
        "password": {
            "type": str,
            "default": None,
            "no_log": True
        },
        "active": {
            "type": bool,
            "default": True
        },
        "default": {
            "type": bool,
            "default": False
        },
        "apply_existing": {
            "type": bool,
            "default": False
        },
        "state": {
            "default": "present",
            "choices": [
                "present",
                "absent"
            ]
        }
    }
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    protocol = params["protocol"]
    host = params["host"]
    port = params["port"]
    state = params["state"]
    options = clear_params(params)

    proxy = get_proxy_by_protocol_host_port(api, protocol, host, port)

    changed = False
    failed_msg = None
    result = {}
    if state == "present":
        if not proxy:
            r = api.add_proxy(**options)
            if not r["ok"]:
                failed_msg = r["msg"]
            changed = True
        else:
            proxy = convert_from_socket(params_map_proxy, proxy)
            changed_keys = object_changed(proxy, options, ["apply_existing"])
            if changed_keys:
                r = api.edit_proxy(proxy["id"], **options)
                if not r["ok"]:
                    failed_msg = r["msg"]
                changed = True
    elif state == "absent":
        if proxy:
            r = api.delete_proxy(proxy["id"])
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
