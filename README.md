# ansible-uptime-kuma

This collection contains modules that allow to configure [Uptime Kuma](https://github.com/louislam/uptime-kuma) with Ansible.

Python version 3.7+ and Ansible version 2.10+ are required.

Supported Uptime Kuma versions:

| Uptime Kuma     | ansible-uptime-kuma | uptime-kuma-api |
|-----------------|---------------------|-----------------|
| 1.21.3          | 1.0.0               | 1.0.0+          |
| 1.17.0 - 1.21.2 | 0.1.0 - 0.14.0      | 0.1.0 - 0.13.0  |


## Installation

This collection requires the python module [uptime-kuma-api](https://github.com/lucasheld/uptime-kuma-api) to communicate with Uptime Kuma. It can be installed using pip:
```shell
pip install uptime-kuma-api
```

Alternately, you can install a specific version (e.g. `0.13.0`):
```shell
pip install uptime-kuma-api==0.13.0
```

Then install the ansible collection itself:
```shell
ansible-galaxy collection install lucasheld.uptime_kuma
```

Alternately, you can install a specific version (e.g. `0.14.0`):
```shell
ansible-galaxy collection install lucasheld.uptime_kuma:==0.14.0
```

## Modules

The following modules are available:

- [api_key](https://github.com/lucasheld/ansible-uptime-kuma/wiki/api_key)
- [api_key_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/api_key_info)
- [docker_host](https://github.com/lucasheld/ansible-uptime-kuma/wiki/docker_host)
- [docker_host_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/docker_host_info)
- [game_list_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/game_list_info)
- [login](https://github.com/lucasheld/ansible-uptime-kuma/wiki/login)
- [maintenance](https://github.com/lucasheld/ansible-uptime-kuma/wiki/maintenance)
- [maintenance_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/maintenance_info)
- [monitor](https://github.com/lucasheld/ansible-uptime-kuma/wiki/monitor)
- [monitor_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/monitor_info)
- [monitor_tag](https://github.com/lucasheld/ansible-uptime-kuma/wiki/monitor_tag)
- [notification](https://github.com/lucasheld/ansible-uptime-kuma/wiki/notification)
- [notification_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/notification_info)
- [proxy](https://github.com/lucasheld/ansible-uptime-kuma/wiki/proxy)
- [proxy_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/proxy_info)
- [settings](https://github.com/lucasheld/ansible-uptime-kuma/wiki/settings)
- [settings_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/settings_info)
- [setup](https://github.com/lucasheld/ansible-uptime-kuma/wiki/setup)
- [status_page](https://github.com/lucasheld/ansible-uptime-kuma/wiki/status_page)
- [status_page_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/status_page_info)
- [tag](https://github.com/lucasheld/ansible-uptime-kuma/wiki/tag)
- [tag_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/tag_info)


## Getting started
Directly after the installation of Uptime Kuma, the initial username and password must be set:
```yaml
- name: Specify the initial username and password
  lucasheld.uptime_kuma.setup:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
```

For future requests you can either use these credentials directly or a token that must be generated once.
The token usage is recommended because frequent logins lead to a rate limit. In this example we create a new monitor.

Option 1 (not recommended): Create a monitor by using the credentials directly:
```yaml
- name: Login with credentials and create a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Google
    type: http
    url: https://google.com
    state: present
```

Option 2 (recommended): Generate a token and create a monitor by using this token:
```yaml
- name: Login with credentials once and register the result
  lucasheld.uptime_kuma.login:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result

- name: Extract the token from the result and set it as fact
  set_fact:
    api_token: "{{ result.token }}"

- name: Login by token and create a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_token: "{{ api_token }}"
    name: Google
    type: http
    url: https://google.com
    state: present
```
