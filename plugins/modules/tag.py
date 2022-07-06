#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args

from uptimekumaapi import UptimeKumaApi

__metaclass__ = type


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add tag
  uptime_kuma_tag:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Tag 1
    color: "#ff0000"
    state: present

- name: Remove tag
  uptime_kuma_tag:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    name: Tag 1
    state: absent
'''

RETURN = r'''
'''


def get_tag_by_name(api, name):
    r = api.get_tags()
    tags = r["tags"]
    for tag in tags:
        if tag["name"] == name:
            return tag


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        color=dict(type="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    name = params["name"]
    color = params["color"]
    state = params["state"]

    tag = get_tag_by_name(api, name)

    changed = False
    failed_msg = None
    result = {}
    if state == "present":
        if not tag:
            r = api.add_tag(color, name)
            if not r["ok"]:
                failed_msg = r["msg"]
            changed = True
    elif state == "absent":
        if tag:
            r = api.delete_tag(tag["id"])
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
