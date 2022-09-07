# Copyright: (c) 2022, Lucas Held <lucasheld@hotmail.de>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def object_changed(obj: dict, options: dict, ignore: dict = None):
    changed_keys = []
    for key, value in options.items():
        if ignore and key in ignore:
            ignore_value = ignore[key]
            if type(ignore_value) == list and value in ignore_value:
                continue
            elif value == ignore_value:
                continue
        if options[key] != obj.get(key):
            changed_keys.append((key, obj.get(key), options[key]))
    return changed_keys


def clear_params(params: dict):
    ignored_params = ["api_url", "api_username", "api_password", "api_token", "state"]
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


def get_docker_host_by_name(api, name):
    docker_hosts = api.get_docker_hosts()
    for docker_host in docker_hosts:
        if docker_host["name"] == name:
            return docker_host


common_module_args = dict(
    api_url=dict(type="str", default="http://127.0.0.1:3001"),
    api_username=dict(type="str"),
    api_password=dict(type="str", no_log=True),
    api_token=dict(type="str", no_log=True)
)
