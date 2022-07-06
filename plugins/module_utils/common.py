def object_changed(object: dict, options: dict, ignore: dict = None):
    changed_keys = []
    for key, value in options.items():
        if ignore and key in ignore:
            ignore_value = ignore[key]
            if type(ignore_value) == list and value in ignore_value:
                continue
            elif value == ignore_value:
                continue
        if options[key] != object.get(key):
            changed_keys.append((key, object.get(key), options[key]))
    return changed_keys


def clear_params(params: dict):
    return {k: v for k, v in params.items() if k not in ["api_url", "api_username", "api_password", "state"]}


def get_proxy_by_protocol_host_port(api, protocol, host, port):
    proxies = api.get_proxies()
    for proxy in proxies:
        if proxy["protocol"] == protocol and proxy["host"] == host and proxy["port"] == port:
            return proxy


def get_notification_by_name(api, name):
    notifications = api.get_notifications()
    for notification in notifications:
        if notification["name"] == name:
            return notification


common_module_args = dict(
    api_url=dict(type="str", default="http://127.0.0.1:3001"),
    api_username=dict(type="str", required=True),
    api_password=dict(type="str", required=True, no_log=True)
)