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

module: status_page
author: Lucas Held (@lucasheld)
short_description: Manages status pages.
description: Manages status pages.

options:
  slug:
    description: The slug of the status page.
    type: str
    required: true
  title:
    description: The title of the status page.
    type: str
  description:
    description: The description of the status page.
    type: str
  theme:
    description: The theme of the status page.
    type: str
    choices: ["light", "dark"]
  published:
    description: True if the status page is published.
    type: bool
  show_tags:
    description: True if the tags are shown.
    type: bool
  domain_name_list:
    description: The domain_name_list of the status page.
    type: list
    elements: "str"
  custom_css:
    description: The custom_css of the status page.
    type: str
  footer_text:
    description: The footer_text of the status page.
    type: str
  show_powered_by:
    description: True if the powered by is shown.
    type: bool
  img_data_url:
    description: The img_data_url of the status page.
    type: str
  monitors:
    description: The monitors of the status page.
    type: list
    elements: "str"
  incident:
    description: The incident of the status page.
    type: dict
    suboptions:
      title:
        description: The title of the status page.
        type: str
        required: true
      content:
        description: The content of the status page.
        type: str
        required: true
      style:
        description: The style of the status page.
        type: str
        choices: ["info", "warning", "danger", "primary", "light", "dark"]
  state:
    description:
      - Set to C(present) to create/update a status page.
      - Set to C(absent) to delete a status page.
    type: str
    default: present
    choices: ["present", "absent"]
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

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args, clear_unset_params

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    slug = params["slug"]
    state = params["state"]

    options = clear_params(params)
    options = clear_unset_params(options)
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
        # id_=dict(type="int"),
        title=dict(type="str"),
        description=dict(type="str"),
        theme=dict(type="str", choices=["light", "dark"]),
        published=dict(type="bool"),
        show_tags=dict(type="bool"),
        domain_name_list=dict(type="list", elements="str"),
        custom_css=dict(type="str"),
        footer_text=dict(type="str"),
        show_powered_by=dict(type="bool"),
        img_data_url=dict(type="str"),
        monitors=dict(type="list", elements="str"),
        incident=dict(type="dict", options=dict(
            title=dict(type="str", required=True),
            content=dict(type="str", required=True),
            style=dict(type="str", choices=["info", "warning", "danger", "primary", "light", "dark"])
        )),
        state=dict(type="str", default="present", choices=["present", "absent"])
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
