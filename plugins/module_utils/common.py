# Copyright: (c) 2023, Lucas Held <lucasheld@hotmail.de>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def object_changed(superset, subset, ignore=None):
    def list_changed(lst2, lst):
        if len(lst2) != len(lst):
            return True
        for i in range(len(lst)):
            if type(lst[i]) == list:
                if list_changed(lst2[i], lst[i]):
                    return True
            elif type(lst[i]) == dict:
                if len(lst2[i]) != len(lst[i]) or object_changed(lst2[i], lst[i]):
                    return True
            else:
                if lst[i] != lst2[i]:
                    return True
        return False

    changed_keys = []
    for key, value in subset.items():
        value2 = superset.get(key)
        if ignore and key in ignore:
            ignore_value = ignore[key]
            if type(ignore_value) == list and value2 in ignore_value:
                continue
            elif value2 == ignore_value:
                continue
            elif ignore_value is None:
                continue
        if type(value) == list:
            if list_changed(value2, value):
                changed_keys.append((key, superset.get(key), subset[key]))
        elif type(value) == dict:
            if len(value2) != len(value) or object_changed(value2, value):
                changed_keys.append((key, superset.get(key), subset[key]))
        else:
            if value != value2:
                changed_keys.append((key, superset.get(key), subset[key]))
    return changed_keys


def clear_params(params: dict):
    ignored_params = [
        "api_url",
        "api_timeout",
        "api_headers",
        "api_ssl_verify",
        "api_wait_events",
        "api_username",
        "api_password",
        "api_token",
        "state"
    ]
    return {k: v for k, v in params.items() if k not in ignored_params}


def clear_unset_params(params: dict):
    return {k: v for k, v in params.items() if v is not None}


def get_proxy_by_host_port(api, host, port):
    proxies = api.get_proxies()
    for proxy in proxies:
        if proxy["host"] == host and proxy["port"] == port:
            return proxy


def get_notification_by_name(api, name):
    notifications = api.get_notifications()
    for notification in notifications:
        if notification["name"] == name:
            return notification


def get_monitor_by_name(api, name):
    monitors = api.get_monitors()
    for monitor in monitors:
        if monitor["name"] == name:
            return monitor


def get_tag_by_name(api, name):
    tags = api.get_tags()
    for tag in tags:
        if tag["name"] == name:
            return tag


def get_monitor_tag(monitor, tag, value):
    for monitor_tag in monitor["tags"]:
        if monitor_tag["name"] == tag["name"] and monitor_tag["color"] == tag["color"] and monitor_tag["value"] == value:
            return monitor_tag


def get_docker_host_by_name(api, name):
    docker_hosts = api.get_docker_hosts()
    for docker_host in docker_hosts:
        if docker_host["name"] == name:
            return docker_host


def get_maintenance_by_title(api, title):
    maintenances = api.get_maintenances()
    for maintenance in maintenances:
        if maintenance["title"] == title:
            return maintenance


def get_api_key_by_name(api, name):
    api_keys = api.get_api_keys()
    for api_key in api_keys:
        if api_key["name"] == name:
            return api_key


common_module_args = dict(
    api_url=dict(type="str", default="http://127.0.0.1:3001"),
    api_timeout=dict(type="float", default=10),
    api_headers=dict(type="dict"),
    api_ssl_verify=dict(type="bool", default=True),
    api_wait_events=dict(type="float", default=0.2),
    api_username=dict(type="str"),
    api_password=dict(type="str", no_log=True),
    api_token=dict(type="str", no_log=True)
)
