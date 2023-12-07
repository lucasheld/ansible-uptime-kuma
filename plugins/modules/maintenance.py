#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Lucas Held <lucasheld@hotmail.de>
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
    choices: ["manual", "single", "recurring-interval", "recurring-weekday", "recurring-day-of-month", "cron"]
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
  cron:
    description: The cron schedule of the maintenance.
    type: str
  durationMinutes:
    description: The duration (in minutes) of the maintenance.
    type: int
  timezoneOption:
    description: The timezone of the maintenance.
    type: str
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
    timezoneOption: "Europe/Berlin"
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
    common_module_args, get_maintenance_by_title, clear_unset_params, get_monitor_by_name

try:
    from uptime_kuma_api import UptimeKumaApi, MaintenanceStrategy
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

        if not params["timeRange"] and params["strategy"] in [
            MaintenanceStrategy.RECURRING_INTERVAL,
            MaintenanceStrategy.RECURRING_WEEKDAY,
            MaintenanceStrategy.RECURRING_DAY_OF_MONTH
        ]:
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
                    monitor_name = monitor.pop("name")
                    r = get_monitor_by_name(api, monitor_name)
                    monitor["id"] = r["id"]

            # add id or name to status page
            for status_page in status_pages:
                if "id" not in status_page:
                    status_page_name = status_page.pop("title")
                    r = get_status_page_by(api, "title", status_page_name)
                    status_page["id"] = r["id"]

            # add monitors to maintenance if changed
            monitors_old = api.get_monitor_maintenance(maintenance_id)
            if sorted([tuple(i.items()) for i in monitors_old]) != sorted([tuple(i.items()) for i in monitors]):
                api.add_monitor_maintenance(maintenance_id, monitors)

            # add status pages to maintenance if changed
            status_pages_old = api.get_status_page_maintenance(maintenance_id)
            if sorted([tuple(i.items()) for i in status_pages_old]) != sorted([tuple(i.items()) for i in status_pages]):
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
        strategy=dict(type="str", choices=["manual", "single", "recurring-interval", "recurring-weekday", "recurring-day-of-month", "cron"]),
        active=dict(type="bool"),
        description=dict(type="str"),
        dateRange=dict(type="list"),
        intervalDay=dict(type="int"),
        weekdays=dict(type="list"),
        daysOfMonth=dict(type="list"),
        timeRange=dict(type="list"),
        cron=dict(type="str"),
        durationMinutes=dict(type="int"),
        timezoneOption=dict(type="str"),
        monitors=dict(type="list"),
        status_pages=dict(type="list"),
        state=dict(type="str", default="present", choices=["present", "absent", "paused", "resumed"])
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
