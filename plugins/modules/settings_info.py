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

module: settings_info
author: Lucas Held (@lucasheld)
short_description: Retrieves facts about settings.
description: Retrieves facts about settings.
'''

EXAMPLES = r'''
- name: get settings
  lucasheld.uptime_kuma.settings_info:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result
'''

RETURN = r'''
settings:
  description: The settings as list
  returned: always
  type: complex
  contains:
    checkUpdate:
      description: Value of the checkUpdate setting.
      returned: always
      type: bool
      sample: true
    checkBeta:
      description: Value of the checkBeta setting.
      returned: always
      type: bool
      sample: false
    keepDataPeriodDays:
      description: Value of the keepDataPeriodDays setting.
      returned: always
      type: int
      sample: 180
    entryPage:
      description: Value of the entryPage setting.
      returned: always
      type: str
      sample: dashboard
    searchEngineIndex:
      description: Value of the searchEngineIndex setting.
      returned: always
      type: bool
      sample: false
    serverTimezone:
      description: Value of the serverTimezone setting.
      returned: always
      type: str
      sample: Europe/Berlin
    primaryBaseURL:
      description: Value of the primaryBaseURL setting.
      returned: always
      type: str
      sample: 
    steamAPIKey:
      description: Value of the steamAPIKey setting.
      returned: always
      type: str
      sample: 
    tlsExpiryNotifyDays:
      description: Value of the tlsExpiryNotifyDays setting.
      returned: always
      type: list
      sample: [7, 14, 21]
    disableAuth:
      description: Value of the disableAuth setting.
      returned: always
      type: bool
      sample: false
    dnsCache:
      description: Value of the dnsCache setting.
      returned: always
      type: bool
      sample: true
    trustProxy:
      description: Value of the trustProxy setting.
      returned: always
      type: bool
      sample: false
    chromeExecutable:
      description: Value of the chromeExecutable setting.
      returned: always
      type: str
      sample: ''
    nscd:
      description: Value of the nscd setting.
      returned: always
      type: bool
      sample: false
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
    result["settings"] = api.get_settings()


def main():
    module_args = dict()
    module_args.update(common_module_args)

    module = AnsibleModule(module_args, supports_check_mode=True)
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
