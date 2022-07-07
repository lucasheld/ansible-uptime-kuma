#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_monitor_by_name, get_tag_by_name

import traceback

from uptimekumaapi import UptimeKumaApi

__metaclass__ = type


# monitor tag edit not possible, because we are using the tag name and value to identify the monitor tag
# so you have to delete the moninor tag first and crete a new one


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add monitor tag
  lucasheld.uptime_kuma.monitor_tag:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    monitor_name: Peer 1
    tag_name: Tag 1
    value: Tag value
    state: present

- name: Remove monitor tag
  lucasheld.uptime_kuma.monitor_tag:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    monitor_name: Peer 1
    tag_name: Tag 1
    value: Tag Value
    state: absent
'''

RETURN = r'''
'''


def get_monitor_tag(monitor, tag, value):
    for monitor_tag in monitor["tags"]:
        if monitor_tag["name"] == tag["name"] and monitor_tag["color"] == tag["color"] and monitor_tag["value"] == value:
            return monitor_tag


def run(api, params, result):
    monitor_name = params["monitor_name"]
    tag_name = params["tag_name"]
    value = params["value"]
    state = params["state"]

    monitor = get_monitor_by_name(api, monitor_name)
    tag = get_tag_by_name(api, tag_name)

    tag_id = tag["id"]
    monitor_id = monitor["id"]

    monitor_tag = get_monitor_tag(monitor, tag, value)

    if state == "present":
        if not monitor_tag:
            api.add_monitor_tag(tag_id, monitor_id, value)
            result["changed"] = True
    elif state == "absent":
        if monitor_tag:
            api.delete_monitor_tag(tag_id, monitor_id, value)
            result["changed"] = True


def main():
    module_args = dict(
        monitor_name=dict(type="str", required=True),
        tag_name=dict(type="str", required=True),
        value=dict(type="str", required=True),
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
