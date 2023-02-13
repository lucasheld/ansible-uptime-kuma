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

module: status_page_info
author: Lucas Held (@lucasheld)
short_description: Retrieves facts about status pages.
description: Retrieves facts about status pages.

options:
  slug:
    description: The slug of the status page to inspect.
    type: str
'''

EXAMPLES = r'''
- name: get all status_pages
  lucasheld.uptime_kuma.status_page_info:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result
'''

RETURN = r'''
status_pages:
  description: The status pages as list
  returned: always
  type: complex
  contains:
    id:
      description: The id of the status page.
      returned: always
      type: int
      sample: 4
    slug:
      description: The slug of the status page.
      returned: always
      type: str
      sample: slug1
    title:
      description: The title of the status page.
      returned: always
      type: str
      sample: status page 1
    description:
      description: The description of the status page.
      returned: always
      type: str
      sample: description 1
    icon:
      description: The icon of the status page.
      returned: always
      type: str
      sample: /icon.svg
    theme:
      description: The theme of the status page.
      returned: always
      type: int
      sample: light
    published:
      description: True if the status page is published.
      returned: always
      type: bool
      sample: True
    showTags:
      description: True if the show tags is enabled.
      returned: always
      type: bool
      sample: False
    domainNameList:
      description: The domain name list of the status page.
      returned: always
      type: list
      sample: []
    googleAnalyticsId:
      description: The Google Analytics ID of the status page.
      returned: always
      type: str
      sample: None
    customCSS:
      description: The custom CSS of the status page.
      returned: always
      type: str
      sample: None
    footerText:
      description: The footer text of the status page.
      returned: always
      type: str
      sample: None
    showPoweredBy:
      description: True if the show powered by is enabled.
      returned: always
      type: bool
      sample: False
    incident:
      description: The incident of the status page.
      returned: always
      type: dict
      sample: {'id': 2, 'style': 'danger', 'title': 'sample title', 'content': 'sample content', 'pin': 1, 'createdDate': '2022-08-26 12:07:00', 'lastUpdatedDate': None}
    maintenanceList:
      description: The maintenance list of the status page.
      returned: always
      type: list
      sample: []
    publicGroupList:
      description: The public group list of the status page.
      returned: always
      type: list
      sample: [{'id': 5, 'name': 'Services', 'weight': 1, 'monitorList': [{'id': 18, 'maintenance': False, 'name': 'sample monitor'}]}]
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args
from ansible.module_utils.basic import missing_required_lib

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    if params["slug"]:
        status_page = api.get_status_page(params["slug"])
        result["status_pages"] = [status_page]
    else:
        result["status_pages"] = api.get_status_pages()


def main():
    module_args = dict(
        slug=dict(type="str"),
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args, supports_check_mode=True)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
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
