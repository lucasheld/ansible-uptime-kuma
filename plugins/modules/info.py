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

module: info
version_added: 0.0.0
author: Lucas Held (@lucasheld)
short_description: Return information about the Uptime Kuma instance
description: Return information about the Uptime Kuma instance

options:
  monitors:
    description: Return monitors.
    type: bool
  notifications:
    description: Return notifications.
    type: bool
  proxies:
    description: Return proxies.
    type: bool
  status_pages:
    description: Return status pages.
    type: bool
  heartbeats:
    description: Return heartbeats.
    type: bool
  important_heartbeats:
    description: Return important heartbeats.
    type: bool
  avg_ping:
    description: Return avg ping.
    type: bool
  uptime:
    description: Return uptime.
    type: bool
  heartbeat:
    description: Return heartbeat.
    type: bool
  info:
    description: Return info.
    type: bool
  monitor_beats:
    description: Return monitor beats.
    type: bool
  tags:
    description: Return tags.
    type: bool
'''

EXAMPLES = r'''
- name: list monitors
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    monitors: yes
  register: result

- name: list notifications
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    notifications: yes
  register: result

- name: list proxies
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    proxies: yes
  register: result

- name: list status pages
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    status_pages: yes
  register: result

- name: list heartbeats
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    heartbeats: yes
  register: result

- name: list important heartbeats
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    important_heartbeats: yes
  register: result

- name: list avg ping
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    avg_ping: yes
  register: result

- name: list uptime
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    uptime: yes
  register: result

- name: list heartbeat
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    heartbeat: yes
  register: result

- name: list info
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    info: yes
  register: result

- name: list monitor beats
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    monitor_beats: yes
  register: result

- name: list tags
  lucasheld.uptime_kuma.info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
    tags: yes
  register: result
'''

RETURN = r'''
monitors:
  description: monitors
    returned: success
    type: str
    sample: []
notifications:
  description: notifications
    returned: success
    type: str
    sample: []
proxies:
  description: proxies
    returned: success
    type: str
    sample: []
status_pages:
  description: status pages
    returned: success
    type: str
    sample: []
heartbeats:
  description: heartbeats
    returned: success
    type: str
    sample: []
important_heartbeats:
  description: important hearts
    returned: success
    type: str
    sample: []
avg_ping:
  description: avg ping
    returned: success
    type: str
    sample: []
uptime:
  description: uptime
    returned: success
    type: str
    sample: []
heartbeat:
  description: heartbeat
    returned: success
    type: str
    sample: []
info:
  description: info
    returned: success
    type: str
    sample: []
monitor_beats:
  description: monitor beats
    returned: success
    type: str
    sample: []
tags:
  description: tags
    returned: success
    type: str
    sample: []
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
    if params.get("monitors"):
        r = api.get_monitors()
        result["monitors"] = r
    if params.get("notifications"):
        r = api.get_notifications()
        result["notifications"] = r
    if params.get("proxies"):
        r = api.get_proxies()
        result["proxies"] = r
    if params.get("status_pages"):
        r = api.get_status_pages()
        result["status_pages"] = r
    if params.get("heartbeats"):
        r = api.get_heartbeats()
        result["heartbeats"] = r
    if params.get("important_heartbeats"):
        r = api.get_important_heartbeats()
        result["important_heartbeats"] = r
    if params.get("avg_ping"):
        r = api.avg_ping()
        result["avg_ping"] = r
    if params.get("uptime"):
        r = api.uptime()
        result["uptime"] = r
    if params.get("heartbeat"):
        r = api.get_heartbeat()
        result["heartbeat"] = r
    if params.get("monitor_beats"):
        r = api.get_monitor_beats()
        result["monitor_beats"] = r
    if params.get("info"):
        r = api.info()
        result["info"] = r
    if params.get("tags"):
        r = api.get_tags()
        result["tags"] = r


def main():
    module_args = dict(
        monitors=dict(type="bool"),
        notifications=dict(type="bool"),
        proxies=dict(type="bool"),
        status_pages=dict(type="bool"),
        heartbeats=dict(type="bool"),
        important_heartbeats=dict(type="bool"),
        avg_ping=dict(type="bool"),
        uptime=dict(type="bool"),
        heartbeat=dict(type="bool"),
        info=dict(type="bool"),
        monitor_beats=dict(type="bool"),
        tags=dict(type="bool"),
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    result = {
        "changed": True
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
