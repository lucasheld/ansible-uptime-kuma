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

module: maintenance_info
author: Lucas Held (@lucasheld)
short_description: Retrieves facts about maintenances.
description: Retrieves facts about maintenances.

options:
  id:
    description:
      - The id of the maintenance to inspect.
      - Only required if no I(title) specified.
    type: int
  title:
    description:
      - The name of the maintenance to inspect.
      - Only required if no I(id) specified.
    type: str
'''

EXAMPLES = r'''
- name: get all maintenances
  lucasheld.uptime_kuma.maintenance_info:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result
'''

RETURN = r'''
maintenances:
  description: The maintenances as list
  returned: always
  type: complex
  contains:
    id:
      description: The id of the maintenance.
      returned: always
      type: int
      sample: 1
    title:
      description: The title of the maintenance.
      returned: always
      type: str
      sample: 'maintenance 1'
    description:
      description: The description of the maintenance.
      returned: always
      type: str
      sample: 'description'
    strategy:
      description: The strategy of the maintenance.
      returned: always
      type: str
      sample: 'single'
    intervalDay:
      description: The interval day of the maintenance.
      returned: always
      type: int
      sample: 1
    active:
      description: True if the maintenance is active.
      returned: always
      type: bool
      sample: true
    dateRange:
      description: The date range of the maintenance.
      returned: always
      type: list
      sample: ["2022-12-27 15:39:00","2022-12-30 15:39:00"]
    timeRange:
      description: The time range of the maintenance.
      returned: always
      type: list
      sample: [{"hours": 2,"minutes": 0,"seconds": 0},{"hours": 3,"minutes": 0,"seconds": 0}]
    weekdays:
      description: The time range of the maintenance.
      returned: always
      type: list
      sample: []
    daysOfMonth:
      description: The days of month of the maintenance.
      returned: always
      type: list
      sample: []
    timeslotList:
      description: The timeslot list of the maintenance.
      returned: always
      type: list
      sample: [{"id": 1,"startDate": "2022-12-27 14:39:00","endDate": "2022-12-30 14:39:00","startDateServerTimezone": "2022-12-27 15:39","endDateServerTimezone": "2022-12-30 15:39","serverTimezoneOffset": "+01:00"}]
    status:
      description: The status of the maintenance.
      returned: always
      type: str
      sample: "under-maintenance"
    monitors:
      description: The monitors of the maintenance.
      returned: If I(id) or I(title) specified.
      type: list
      sample: [{"id": 1,"name": "monitor 1"}]
    status_pages:
      description: The status pages of the maintenance.
      returned: If I(id) or I(title) specified.
      type: list
      sample: [{"id": 1,"title": "status page 1"}]
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_maintenance_by_title
from ansible.module_utils.basic import missing_required_lib

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def add_maintenance_monitors_status_pages(api, maintenance):
    maintenance_id = maintenance["id"]
    maintenance_monitors = api.get_monitor_maintenance(maintenance_id)
    maintenance_status_pages = api.get_status_page_maintenance(maintenance_id)
    maintenance.update({
        "monitors": maintenance_monitors,
        "status_pages": maintenance_status_pages
    })


def run(api, params, result):
    if params["id"]:
        maintenance = api.get_maintenance(params["id"])
        add_maintenance_monitors_status_pages(api, maintenance)
        maintenances = [maintenance]
    elif params["title"]:
        maintenance = get_maintenance_by_title(api, params["title"])
        add_maintenance_monitors_status_pages(api, maintenance)
        maintenances = [maintenance]
    else:
        maintenances = api.get_maintenances()

    result["maintenances"] = maintenances


def main():
    module_args = dict(
        id=dict(type="int"),
        title=dict(type="str"),
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
