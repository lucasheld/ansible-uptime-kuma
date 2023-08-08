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

module: settings
author: Lucas Held (@lucasheld)
short_description: Manages settings.
description: Manages settings.

options:
  password:
    description:
      - The Uptime Kuma password.
      - Only required if I(disableAuth) is true.
    type: str
  checkUpdate:
    description: True if update check should be enabled.
    type: bool
  checkBeta:
    description: True if update check for beta versions should be enabled.
    type: bool
  keepDataPeriodDays:
    description: Keep monitor history data for this number of days.
    type: int
  serverTimezone:
    description: The server timezone.
    type: str
  entryPage:
    description: The entry page. The value requires the prefix "statusPage-". For example, if the slug is "1uhosting", then the entryPage is "statusPage-1uhosting".
    type: str
  searchEngineIndex:
    description: True if Uptime Kuma should be indexed by search engines.
    type: bool
  primaryBaseURL:
    description: The primary base URL.
    type: str
  steamAPIKey:
    description: The Steam API key for monitoring a Steam game server.
    type: str
  dnsCache:
    description: True if dns cache should be enabled.
    type: bool
  tlsExpiryNotifyDays:
    description: HTTPS monitors trigger notification when the TLS certificate expires in the specified days.
    type: list
    elements: int
  disableAuth:
    description: True if authentication should be disabled.
    type: bool
  trustProxy:
    description:
      - True to trust 'X-Forwarded-*' headers.
      - If you want to get the correct client IP and your Uptime Kuma is behind such as Nginx or Apache, you should enable this.
    type: bool
'''

EXAMPLES = r'''
- name: Enable beta version update check
  lucasheld.uptime_kuma.settings:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    checkBeta: true
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, object_changed, \
    clear_params, clear_unset_params

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    options = clear_params(params)
    options = clear_unset_params(options)

    settings = api.get_settings()

    changed_keys = object_changed(settings, options)
    if changed_keys:
        api.set_settings(**options)
        result["changed"] = True


def main():
    module_args = dict(
        password=dict(type="str", no_log=True),
        # about
        checkUpdate=dict(type="bool"),
        checkBeta=dict(type="bool"),
        # monitor history
        keepDataPeriodDays=dict(type="int"),
        # general
        serverTimezone=dict(type="str"),
        entryPage=dict(type="str"),
        searchEngineIndex=dict(type="bool"),
        primaryBaseURL=dict(type="str"),
        steamAPIKey=dict(type="str"),
        dnsCache=dict(type="bool"),
        # notifications
        tlsExpiryNotifyDays=dict(type="list", elements="int"),
        # security
        disableAuth=dict(type="bool"),
        # reverse proxy
        trustProxy=dict(type="bool"),
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
