# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = '''
options:
  api_url:
    description: The Uptime Kuma URL.
    type: str
    default: http://127.0.0.1:3001
  api_timeout:
    description: How many seconds the client should wait for the connection, an expected event or a server response.
    type: float
    default: 10
  api_headers:
    description: Headers that are passed to the socketio connection.
    type: dict
  api_ssl_verify:
    description:
      - true to verify SSL certificates, or false to skip SSL certificate verification,
      - allowing connections to servers with self signed certificates.
    type: bool
    default: true
  api_wait_events:
    description:
      - How many seconds the client should wait for the next event of the same type.
      - There is no way to determine when the last message of a certain type has arrived. Therefore, a timeout is required.
      - If no further message has arrived within this time, it is assumed that it was the last message.
    type: float
    default: 0.2
  api_username:
    description:
      - The Uptime Kuma username.
      - Only required if no I(api_token) specified and authentication is enabled.
    type: str
  api_password:
    description:
      - The Uptime Kuma password.
      - Only required if no I(api_token) specified and authentication is enabled.
    type: str
  api_token:
    description:
      - The Uptime Kuma login token.
      - Only required if no I(api_username) and I(api_password) specified and authentication is enabled.
    type: str

requirements:
  - uptime-kuma-api
'''
