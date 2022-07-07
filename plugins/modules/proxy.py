#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args, get_proxy_by_protocol_host_port

import traceback

from uptime_kuma_api import UptimeKumaApi

__metaclass__ = type


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add proxy
  lucasheld.uptime_kuma.proxy:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    protocol: http
    host: 127.0.0.1
    port: 8080
    state: present

- name: Edit proxy
  lucasheld.uptime_kuma.proxy:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    protocol: https
    host: 127.0.0.1
    port: 8080
    state: present

- name: Remove proxy
  lucasheld.uptime_kuma.proxy:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    protocol: http
    host: 127.0.0.1
    port: 8080
    state: absent
'''

RETURN = r'''
'''

def run(api, params, result):
    state = params["state"]
    options = clear_params(params)

    proxy = get_proxy_by_protocol_host_port(api, params["protocol"], params["host"], params["port"])

    if state == "present":
        if not proxy:
            api.add_proxy(**options)
            result["changed"] = True
        else:
            changed_keys = object_changed(proxy, options, {"apply_existing": [False, None]})
            if changed_keys:
                api.edit_proxy(proxy["id"], **options)
                result["changed"] = True
    elif state == "absent":
        if proxy:
            api.delete_proxy(proxy["id"])
            result["changed"] = True


def main():
    module_args = dict(
        protocol=dict(type="str", required=True),
        host=dict(type="str", required=True),
        port=dict(type="int", required=True),
        auth=dict(type="bool", default=False),
        username=dict(type="str", default=None),
        password=dict(type="str", default=None, no_log=True),
        active=dict(type="bool", default=True),
        default=dict(type="bool", default=False),
        apply_existing=dict(type="bool", default=False),
        state=dict(type="str", default="present", choices=["present", "absent"])
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
