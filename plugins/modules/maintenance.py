#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import datetime

DOCUMENTATION = r'''
---
extends_documentation_fragment:
  - lucasheld.uptime_kuma.uptime_kuma

module: maintenance
author: Lucas Held (@lucasheld)
short_description: Manages maintenances.
description: Manages maintenances.

options:
  id:
    description:
      - The id of the maintenance.
      - Only required if no I(title) specified.
    type: int
  title:
    description:
      - The title of the maintenance.
      - Only required if no I(id) specified.
    type: str
  strategy:
    description: The strategy of the maintenance.
    type: str
    choices: ["manual", "single", "recurring-interval", "recurring-weekday", "recurring-day-of-month"]
  active:
    description: True if the maintenance is active.
    type: bool
  description:
    description: The description of the maintenance.
    type: str
  dateRange:
    description: The date range of the maintenance.
    type: list
    elements: str
  intervalDay:
    description: The interval day of the maintenance.
    type: int
  weekdays:
    description: The weekdays of the maintenance.
    type: list
    elements: int
  daysOfMonth:
    description: The weekdays of the maintenance.
    type: list
  timeRange:
    description: The time range of the maintenance.
    type: list
  monitors:
    description: The monitors of the maintenance.
    type: list
  status_pages:
    description: The status pages of the maintenance.
    type: list
'''

EXAMPLES = r'''
- name: Add a maintenance
  lucasheld.uptime_kuma.maintenance:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    title: maintenance 1
    description: test
    strategy: single
    active: true
    intervalDay: 1
    dateRange:
      - "2022-12-27 22:36:00"
      - "2022-12-29 22:36:00"
    timeRange:
      - hours: 2
        minutes: 0
      - hours: 3
        minutes: 0
    monitors:
      - name: monitor 1
      - name: monitor 2
    status_pages:
      - name: status page 1
      - name: status page 2
    state: present

- name: Edit a maintenance
  lucasheld.uptime_kuma.maintenance:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    title: maintenance 1
    description: test
    strategy: recurring-interval
    active: true
    intervalDay: 1
    dateRange:
      - "2022-12-27 22:37:00"
      - "2022-12-29 22:37:00"
    timeRange:
      - hours: 2
        minutes: 0
      - hours: 3
        minutes: 0
    monitors:
      - id: 1
    status_pages:
      - id: 1
    state: present

- name: Remove a maintenance
  lucasheld.uptime_kuma.maintenance:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    title: maintenance 1
    state: absent

- name: Pause a maintenance
  lucasheld.uptime_kuma.maintenance:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    title: maintenance 1
    state: paused

- name: Resume a maintenance
  lucasheld.uptime_kuma.maintenance:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    title: maintenance 1
    state: resumed
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, \
    common_module_args, get_proxy_by_host_port, get_notification_by_name, get_maintenance_by_title, clear_unset_params, \
    get_docker_host_by_name, get_monitor_by_name

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def get_status_page_by(api, key, value):
    status_pages = api.get_status_pages()
    for status_page in status_pages:
        if status_page[key] == value:
            return status_page


def run(api, params, result):
    if not params["dateRange"]:
        params["dateRange"] = [
            datetime.date.today().strftime("%Y-%m-%d 00:00:00")
        ]

    if not params["timeRange"]:
        params["timeRange"] = [
            {
                "hours": 2,
                "minutes": 0,
            },
            {
                "hours": 3,
                "minutes": 0,
            }
        ]

    if not params["weekdays"]:
        params["weekdays"] = []

    if not params["daysOfMonth"]:
        params["daysOfMonth"] = []

    state = params["state"]
    options = clear_params(params)
    options = clear_unset_params(options)
    if "monitors" in options:
        del options["monitors"]
    if "status_pages" in options:
        del options["status_pages"]

    if params["id"]:
        maintenance = api.get_maintenance(params["id"])
    else:
        maintenance = get_maintenance_by_title(api, params["title"])

    if state == "present":
        if not maintenance:
            r = api.add_maintenance(**options)
            maintenance_id = r["maintenanceID"]
            maintenance = api.get_maintenance(maintenance_id)
            result["changed"] = True
        else:
            maintenance_id = maintenance["id"]
            changed_keys = object_changed(maintenance, options)
            if changed_keys:
                api.edit_maintenance(maintenance["id"], **options)
                result["changed"] = True
        if maintenance:
            monitors = params["monitors"] or []
            status_pages = params["status_pages"] or []

            # add id or name to monitor
            for monitor in monitors:
                if "id" not in monitor:
                    r = get_monitor_by_name(api, monitor["name"])
                    monitor["id"] = r["id"]
                if "name" not in monitor:
                    r = api.get_monitor(monitor["id"])
                    monitor["name"] = r["name"]

            # add id or name to status page
            for status_page in status_pages:
                if "id" not in status_page:
                    r = get_status_page_by(api, "name", status_page["name"])
                    status_page["id"] = r["id"]
                if "name" not in status_page:
                    r = get_status_page_by(api, "id", status_page["id"])
                    status_page["name"] = r["name"]

            # add monitors to maintenance if changed
            monitors_old = api.get_monitor_maintenance(maintenance_id)
            monitors_old.sort()
            monitors.sort()
            if monitors_old != monitors:
                api.add_monitor_maintenance(maintenance_id, monitors)

            # add status pages to maintenance if changed
            status_pages_old = api.get_status_page_maintenance(maintenance_id)
            status_pages_old.sort()
            status_pages.sort()
            if status_pages_old != status_pages:
                api.add_status_page_maintenance(maintenance_id, status_pages)
    elif state == "absent":
        if maintenance:
            api.delete_maintenance(maintenance["id"])
            result["changed"] = True
    elif state == "paused":
        if maintenance and maintenance["active"]:
            api.pause_maintenance(maintenance["id"])
            result["changed"] = True
    elif state == "resumed":
        if maintenance and not maintenance["active"]:
            api.resume_maintenance(maintenance["id"])
            result["changed"] = True


def main():
    module_args = dict(
        id=dict(type="int"),
        title=dict(type="str"),
        strategy=dict(type="str", choices=["manual", "single", "recurring-interval", "recurring-weekday", "recurring-day-of-month"]),
        active=dict(type="bool"),
        description=dict(type="str"),
        dateRange=dict(type="list"),
        intervalDay=dict(type="int"),
        weekdays=dict(type="list"),
        daysOfMonth=dict(type="list"),
        timeRange=dict(type="list"),
        monitors=dict(type="list"),
        status_pages=dict(type="list"),
        state=dict(type="str", default="present", choices=["present", "absent", "paused", "resumed"])
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
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
