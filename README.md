# ansible-uptime-kuma

This collection contains modules that allow to configure Uptime Kuma with Ansible.

Python version 3.6+ is required.

## Installation

This collection requires the python module [uptime-kuma-api](https://github.com/lucasheld/uptime-kuma-api) to communicate with Uptime Kuma. It can be installed using pip:
```shell
pip install uptime-kuma-api
```

Then install the ansible collection itself:
```shell
ansible-galaxy collection install git+https://github.com/lucasheld/ansible-uptime-kuma.git
```

## Modules

The following modules are available:

- [monitor](https://github.com/lucasheld/ansible-uptime-kuma/wiki/monitor)
- [monitor_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/monitor_info)
- [monitor_tag](https://github.com/lucasheld/ansible-uptime-kuma/wiki/monitor_tag)
- [notification](https://github.com/lucasheld/ansible-uptime-kuma/wiki/notification)
- [notification_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/notification_info)
- [proxy](https://github.com/lucasheld/ansible-uptime-kuma/wiki/proxy)
- [proxy_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/proxy_info)
- [setup](https://github.com/lucasheld/ansible-uptime-kuma/wiki/setup)
- [status_page](https://github.com/lucasheld/ansible-uptime-kuma/wiki/status_page)
- [status_page_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/status_page_info)
- [tag](https://github.com/lucasheld/ansible-uptime-kuma/wiki/tag)
- [tag_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/tag_info)
