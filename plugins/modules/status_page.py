#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args

import traceback

from uptimekumaapi import UptimeKumaApi

__metaclass__ = type


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add status page
  lucasheld.uptime_kuma.status_page:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    slug: testslug
    title: testtitle
    state: present

- name: Edit status page
  lucasheld.uptime_kuma.status_page:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    slug: testslug
    title: newtitle
    incident:
      title: incidenttitle
      content: incidentcontent
      style: info
    state: present

- name: Remove status page
  lucasheld.uptime_kuma.status_page:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    slug: testslug
    state: absent
'''

RETURN = r'''
'''


def run(api, params, result):
    slug = params["slug"]
    state = params["state"]

    options = clear_params(params)
    del options["incident"]

    try:
        status_page = api.get_status_page(slug)
    except Exception:
        status_page = None

    if state == "present":
        status_page_exists = True if status_page else False
        if not status_page:
            api.add_status_page(slug, params["title"])
            api.save_status_page(**options)
            status_page_exists = True
            result["changed"] = True
        else:
            changed_keys = object_changed(status_page, options, {"custom_css": "body {\n  \n}\n"})
            if changed_keys:
                api.save_status_page(**options)
                result["changed"] = True
        if status_page_exists:
            if params["incident"]:
                api.post_incident(slug, **params["incident"])
            else:
                api.unpin_incident(slug)
            # There is no way to check if an incident is already pinned or not. So we have to assume that something has been changed.
            result["changed"] = True
    elif state == "absent":
        if status_page:
            api.delete_status_page(slug)
            result["changed"] = True


def main():
    module_args = dict(
        slug=dict(type="str", required=True),

        # TODO
        # id_=dict(type="int"),

        title=dict(type="str"),
        description=dict(type="str", default=None),
        theme=dict(type="str", default="light", choices=["light", "dark"]),
        published=dict(type="bool", default=True),
        show_tags=dict(type="bool", default=False),
        domain_name_list=dict(type="list", options="str", default=[]),
        custom_css=dict(type="str", default=""),
        footer_text=dict(type="str", default=None),
        show_powered_by=dict(type="bool", default=True),
        img_data_url=dict(type="str", default="/icon.svg"),
        monitors=dict(type="list", options="str", default=None),

        incident=dict(type="dict", default=None, options=dict(
            title=dict(type="str", required=True),
            content=dict(type="str", required=True),
            style=dict(type="str", default="primary", choices=["info", "warning", "danger", "primary", "light", "dark"])
        )),

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
