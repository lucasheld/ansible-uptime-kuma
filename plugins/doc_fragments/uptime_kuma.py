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
  api_wait_timeout:
    description: "How many seconds the client should wait for the connection (default: 1)."
    type: float
    default: 1
  api_headers:
    description: Headers that are passed to the socketio connection.
    type: dict
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
