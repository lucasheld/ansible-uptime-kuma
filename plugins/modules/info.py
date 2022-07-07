#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args

import traceback

from uptimekumaapi import UptimeKumaApi

__metaclass__ = type


# not implemented:
# get_settings
# get_database_size
# monitor_beats - need params


DOCUMENTATION = r'''
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
'''


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
        tags=dict(type="bool"),
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

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
