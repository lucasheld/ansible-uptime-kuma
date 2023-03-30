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

module: monitor
author: Lucas Held (@lucasheld)
short_description: Manages monitors.
description: Manages monitors.

options:
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
  description:
    description: The description of the monitor.
    type: str
  type:
    description: The type of the monitor.
    type: str
    choices: ["http", "port", "ping", "keyword", "grpc-keyword", "dns", "docker", "push", "steam", "gamedig", "mqtt", "sqlserver", "postgres", "mysql", "mongodb", "radius", "redis"]
  interval:
    description: The heartbeat interval of the monitor.
    type: int
  retryInterval:
    description: The heartbeat retry interval of the monitor.
    type: int
  resendInterval:
    description: The heartbeat resend interval of the monitor.
    type: int
  maxretries:
    description: The max retries of the monitor.
    type: int
  upsideDown:
    description: True if upside down mode is enabled.
    type: bool
  notificationIDList:
    description:
      - The notification ids of the monitor.
      - Only required if I(notification_names) not specified.
    type: list
    elements: int
  notification_names:
    description:
      - The notification names of the monitor.
      - Only required if I(notificationIDList) not specified.
    type: list
    elements: str
  httpBodyEncoding:
    description: The body encoding of the monitor.
    type: str
  url:
    description: The url of the monitor.
    type: str
  expiryNotification:
    description: True if certificate expiry notification is enabled.
    type: bool
  ignoreTls:
    description: True if ignore tls error is enabled.
    type: bool
  maxredirects:
    description: The redirects of the monitor.
    type: int
  accepted_statuscodes:
    description: The accepted status codes of the monitor.
    type: list
    elements: str
  proxyId:
    description:
      - The proxy id of the monitor.
      - Only required if no I(proxy) specified.
    type: int
  proxy:
    description: The proxy of the monitor.
    type: dict
    suboptions:
      host:
        description:
          - The host of the proxy.
          - Only required if no I(proxyId) specified.
        type: str
      port:
        description:
          - The port of the proxy.
          - Only required if no I(proxyId) specified.
        type: int
  method:
    description: The http method of the monitor.
    type: str
  body:
    description: The http body of the monitor.
    type: str
  headers:
    description: The http headers of the monitor.
    type: str
  authMethod:
    description: The auth method of the monitor.
    type: str
    choices: ["", "basic", "ntlm", "mtls"]
  tlsCert:
    description: The tls cert of the monitor.
    type: str
  tlsKey:
    description: The tls key of the monitor.
    type: str
  tlsCa:
    description: The tls ca of the monitor.
    type: str
  basic_auth_user:
    description: The auth user of the monitor.
    type: str
  basic_auth_pass:
    description: The auth pass of the monitor.
    type: str
  authDomain:
    description: The auth domain of the monitor.
    type: str
  authWorkstation:
    description: The auth workstation of the monitor.
    type: str
  keyword:
    description: The keyword of the monitor.
    type: str
  grpcUrl:
    description: The grpc url of the monitor.
    type: str
  grpcEnableTls:
    description: True to enable grpc tls.
    type: bool
  grpcServiceName:
    description: The grpc service name of the monitor.
    type: str
  grpcMethod:
    description: The grpc method of the monitor.
    type: str
  grpcProtobuf:
    description: The grpc protobuf of the monitor.
    type: str
  grpcBody:
    description: The grpc body of the monitor.
    type: str
  grpcMetadata:
    description: The grpc metadata of the monitor.
    type: str
  hostname:
    description: The hostname of the monitor.
    type: str
  packetSize:
    description: The packet size of the monitor.
    type: int
  port:
    description: The port of the monitor.
    type: int
  dns_resolve_server:
    description: The dns resolve server of the monitor.
    type: str
  dns_resolve_type:
    description: The dns resolve type of the monitor.
    type: str
  mqttUsername:
    description: The mqtt username of the monitor.
    type: str
  mqttPassword:
    description: The mqtt password of the monitor.
    type: str
  mqttTopic:
    description: The mqtt topic of the monitor.
    type: str
  mqttSuccessMessage:
    description: The mqtt success message of the monitor.
    type: str
  databaseConnectionString:
    description: The sqlserver connection string of the monitor.
    type: str
  databaseQuery:
    description: The sqlserver query of the monitor.
    type: str
  docker_container:
    description: The docker container of the monitor.
    type: str
  docker_host:
    description:
      - The docker host id of the monitor.
      - Only required if no I(docker_host_name) specified.
    type: int
  docker_host_name:
    description:
      - The docker host name of the monitor.
      - Only required if no I(docker_host) specified.
    type: str
  radiusUsername:
    description: The radius username of the monitor.
    type: str
  radiusPassword:
    description: The radius password of the monitor.
    type: str
  radiusSecret:
    description: The radius secret of the monitor.
    type: str
  radiusCalledStationId:
    description: The radius called station id of the monitor.
    type: str
  radiusCallingStationId:
    description: The radius calling station id of the monitor.
    type: str
  game:
    description: The game of the monitor.
    type: str
  state:
    description:
      - Set to C(present) to create/update a monitor.
      - Set to C(absent) to delete a monitor.
      - Set to C(paused) to pause a monitor.
      - Set to C(resumed) to resume a monitor.
    type: str
    default: present
    choices: ["present", "absent", "paused", "resumed"]
'''

EXAMPLES = r'''
- name: Add a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    type: keyword
    name: Monitor 1
    url: http://127.0.0.1
    keyword: healthy
    state: present

- name: Edit a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    type: http
    name: Monitor 1
    url: http://127.0.0.1
    state: present

- name: Remove a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Monitor 1
    state: absent

- name: Pause a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Monitor 1
    state: paused

- name: Resume a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Monitor 1
    state: resumed
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, \
    common_module_args, get_proxy_by_host_port, get_notification_by_name, get_monitor_by_name, clear_unset_params, \
    get_docker_host_by_name

try:
    from uptime_kuma_api import UptimeKumaApi, MonitorType
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    if not params["accepted_statuscodes"]:
        params["accepted_statuscodes"] = ["200-299"]

    if not params["databaseConnectionString"]:
        if params["type"] == MonitorType.SQLSERVER:
            params["databaseConnectionString"] = "Server=<hostname>,<port>;Database=<your database>;User Id=<your user id>;Password=<your password>;Encrypt=<true/false>;TrustServerCertificate=<Yes/No>;Connection Timeout=<int>"
        elif params["type"] == MonitorType.POSTGRES:
            params["databaseConnectionString"] = "postgres://username:password@host:port/database"
        elif params["type"] == MonitorType.MYSQL:
            params["databaseConnectionString"] = "mysql://username:password@host:port/database"
        elif params["type"] == MonitorType.MONGODB:
            params["databaseConnectionString"] = "mongodb://username:password@host:port/database"
        elif params["type"] == MonitorType.REDIS:
            params["databaseConnectionString"] = "redis://user:password@host:port"

    if not params["port"]:
        if type == MonitorType.DNS:
            params["port"] = 53
        elif type == MonitorType.RADIUS:
            params["port"] = 1812

    # notification_names -> notificationIDList
    if params["notification_names"]:
        notification_ids = []
        for notification_name in params["notification_names"]:
            notification = get_notification_by_name(api, notification_name)
            notification_ids.append(notification["id"])
        params["notificationIDList"] = notification_ids
    del params["notification_names"]

    # proxy -> proxyId
    if params["proxy"]:
        proxy = get_proxy_by_host_port(api, params["proxy_id"]["host"], params["proxy_id"]["port"])
        params["proxyId"] = proxy["id"]
    del params["proxy"]

    # docker_host_name -> docker_host
    if params["docker_host_name"]:
        docker_host = get_docker_host_by_name(api, params["docker_host_name"])
        params["docker_host"] = docker_host["id"]
    del params["docker_host_name"]

    state = params["state"]
    options = clear_params(params)
    options = clear_unset_params(options)

    if params["id"]:
        monitor = api.get_monitor(params["id"])
    else:
        monitor = get_monitor_by_name(api, params["name"])

    if state == "present":
        if not monitor:
            api.add_monitor(**options)
            result["changed"] = True
        else:
            changed_keys = object_changed(monitor, options)
            if changed_keys:
                api.edit_monitor(monitor["id"], **options)
                result["changed"] = True
    elif state == "absent":
        if monitor:
            api.delete_monitor(monitor["id"])
            result["changed"] = True
    elif state == "paused":
        if monitor and monitor["active"]:
            api.pause_monitor(monitor["id"])
            result["changed"] = True
    elif state == "resumed":
        if monitor and not monitor["active"]:
            api.resume_monitor(monitor["id"])
            result["changed"] = True


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
        type=dict(type="str", choices=["http", "port", "ping", "keyword", "grpc-keyword", "dns", "docker", "push", "steam", "gamedig", "mqtt", "sqlserver", "postgres", "mysql", "mongodb", "radius", "redis"]),
        description=dict(type="str"),
        interval=dict(type="int"),
        retryInterval=dict(type="int"),
        resendInterval=dict(type="int"),
        maxretries=dict(type="int"),
        upsideDown=dict(type="bool"),
        notificationIDList=dict(type="list", elements="int"),
        notification_names=dict(type="list", elements="str"),
        httpBodyEncoding=dict(type="str"),

        # HTTP, KEYWORD
        url=dict(type="str"),
        expiryNotification=dict(type="bool"),
        ignoreTls=dict(type="bool"),
        maxredirects=dict(type="int"),
        accepted_statuscodes=dict(type="list", elements="str"),
        proxyId=dict(type="int"),
        proxy=dict(type="dict", options=dict(
            host=dict(type="str"),
            port=dict(type="int")
        )),
        method=dict(type="str"),
        body=dict(type="str"),
        headers=dict(type="str"),
        authMethod=dict(type="str", choices=["", "basic", "ntlm", "mtls"]),
        tlsCert=dict(type="str"),
        tlsKey=dict(type="str"),
        tlsCa=dict(type="str"),
        basic_auth_user=dict(type="str"),
        basic_auth_pass=dict(type="str", no_log=True),
        authDomain=dict(type="str"),
        authWorkstation=dict(type="str"),

        # KEYWORD
        keyword=dict(type="str"),

        # GRPC_KEYWORD
        grpcUrl=dict(type="str"),
        grpcEnableTls=dict(type="bool"),
        grpcServiceName=dict(type="str"),
        grpcMethod=dict(type="str"),
        grpcProtobuf=dict(type="str"),
        grpcBody=dict(type="str"),
        grpcMetadata=dict(type="str"),

        # PORT, PING, DNS, STEAM, MQTT
        hostname=dict(type="str"),

        # PING
        packetSize=dict(type="int"),

        # PORT, DNS, STEAM, MQTT, RADIUS
        port=dict(type="int"),

        # DNS
        dns_resolve_server=dict(type="str"),
        dns_resolve_type=dict(type="str"),

        # MQTT
        mqttUsername=dict(type="str"),
        mqttPassword=dict(type="str", no_log=True),
        mqttTopic=dict(type="str"),
        mqttSuccessMessage=dict(type="str"),

        # SQLSERVER, POSTGRES, MYSQL, MONGODB, REDIS
        databaseConnectionString=dict(type="str"),

        # SQLSERVER, POSTGRES, MYSQL
        databaseQuery=dict(type="str"),

        # DOCKER
        docker_container=dict(type="str"),
        docker_host=dict(type="int"),
        docker_host_name=dict(type="str"),

        # RADIUS
        radiusUsername=dict(type="str"),
        radiusPassword=dict(type="str"),
        radiusSecret=dict(type="str"),
        radiusCalledStationId=dict(type="str"),
        radiusCallingStationId=dict(type="str"),

        # GAMEDIG
        game=dict(type="str"),

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
