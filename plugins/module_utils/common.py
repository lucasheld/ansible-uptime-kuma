def object_changed(object, options, ignore=None):
    changed_keys = []
    for key in options.keys():
        if ignore and key in ignore:
            continue
        if options[key] != object.get(key):
            changed_keys.append((key, object.get(key), options[key]))
    return changed_keys


def clear_params(params):
    return {k: v for k, v in params.items() if k not in ["api_url", "api_username", "api_password", "state"]}


common_module_args = {
    "api_url": {
        "type": str,
        "default": "http://127.0.0.1:3001"
    },
    "api_username": {
        "type": str,
        "required": True
    },
    "api_password": {
        "type": str,
        "required": True,
        "no_log": True
    }
}
