#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Lucas Held <lucasheld@hotmail.de>
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
  showTags:
    description: True if the tags are shown.
    type: bool
  domainNameList:
    description: The domain name list of the status page.
    type: list
    elements: "str"
  googleAnalyticsId:
    description: The Google Analytics ID of the status page.
    type: str
  customCSS:
    description: The custom CSS of the status page.
    type: str
  footerText:
    description: The footer text of the status page.
    type: str
  showPoweredBy:
    description: True if the powered by is shown.
    type: bool
  icon:
    description: The icon of the status page.
    type: str
  publicGroupList:
    description: The public group list of the status page.
    type: list
    suboptions:
      name:
        description: The name of the group.
        type: str
        required: true
      weight:
        description: The weight of the group.
        type: int
      monitorList:
        description: The monitor list of the group.
        type: list
        required: true
        suboptions:
          id:
            description:
              - The id of the monitor.
              - Only required if no I(name) specified.
            type: int
          name:
            description:
              - The name of the monitor.
              - Only required if no I(id) specified.
            type: str
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
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    slug: testslug
    title: testtitle
    state: present

- name: Add status page with incident
  lucasheld.uptime_kuma.status_page:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    slug: testslug
    title: newtitle
    incident:
      title: incidenttitle
      content: incidentcontent
      style: info
    state: present

- name: Add status page with monitor
  lucasheld.uptime_kuma.status_page:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    slug: testslug
    title: testtitle
    publicGroupList:
      - name: Services
        weight: 1
        monitorList:
          - name: Monitor 1

- name: Remove status page
  lucasheld.uptime_kuma.status_page:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    slug: testslug
    state: absent
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, \
    common_module_args, clear_unset_params, get_monitor_by_name

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
    if "incident" in options:
        del options["incident"]

    for group in options.get("publicGroupList", []):
        for monitor in group.get("monitorList", []):
            if monitor["id"]:
                monitor.pop("name")
            else:
                monitor_name = monitor.pop("name")
                monitor["id"] = get_monitor_by_name(api, monitor_name)["id"]

    try:
        status_page = api.get_status_page(slug)
    except Exception:
        status_page = None

    if state == "present":
        if not status_page:
            api.add_status_page(slug, params["title"])
            api.save_status_page(**options)
            status_page = api.get_status_page(slug)
            result["changed"] = True
        else:
            changed_keys = object_changed(status_page, options, {"customCSS": "body {\n  \n}\n"})
            if changed_keys:
                api.save_status_page(**options)
                result["changed"] = True
        if status_page:
            status_page_incident = status_page.get("incident")
            if params["incident"]:
                if not status_page_incident:
                    api.post_incident(slug, **params["incident"])
                    result["changed"] = True
            else:
                if status_page_incident:
                    api.unpin_incident(slug)
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
        showTags=dict(type="bool"),
        domainNameList=dict(type="list", elements="str"),
        googleAnalyticsId=dict(type="str"),
        customCSS=dict(type="str"),
        footerText=dict(type="str"),
        showPoweredBy=dict(type="bool"),
        icon=dict(type="str"),
        publicGroupList=dict(type="list", elements="dict", options=dict(
            name=dict(type="str", required=True),
            weight=dict(type="int", required=False),
            monitorList=dict(type="list", elements="dict", options=dict(
                id=dict(type="int", required=False),
                name=dict(type="str", required=False)
            ))
        )),
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

    api = UptimeKumaApi(params["api_url"], timeout=params["api_timeout"], headers=params["api_headers"], ssl_verify=params["api_ssl_verify"], wait_events=params["api_wait_events"])
    api_token = params.get("api_token")
    api_username = params.get("api_username")
    api_password = params.get("api_password")
    if api_token:
        api.login_by_token(api_token)
    elif api_username and api_password:
        api.login(api_username, api_password)
    else:
        # autoLogin for enabled disableAuth
        api.login()

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
