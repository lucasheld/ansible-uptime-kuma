# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Lucas Held <lucasheld@hotmail.de>
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
  api_username:
    description:
      - The Uptime Kuma username.
      - Only required if no I(api_token) specified.
    type: str
  api_password:
    description:
      - The Uptime Kuma password.
      - Only required if no I(api_token) specified.
    type: str
  api_token:
    description:
      - The Uptime Kuma login token.
      - Only required if no I(api_username) and I(api_password) specified.
    type: str

requirements:
  - uptime-kuma-api
'''
