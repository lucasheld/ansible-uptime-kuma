#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
extends_documentation_fragment:
  - lucasheld.uptime_kuma.uptime_kuma

module: notification_info
author: Lucas Held (@lucasheld)
short_description: Retrieves facts about a notification.
description: Retrieves facts about a notification.

options:
  id:
    description: The id of the notification to inspect.
    type: int
  name:
    description: The name of the notification to inspect.
    type: str
'''

EXAMPLES = r'''
- name: get all notifications
  lucasheld.uptime_kuma.notification_info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
  register: result
'''

RETURN = r'''
notifications:
  description: The notifications as list
  returned: always
  type: complex
  contains:
    id:
      description: The id of the notification.
      returned: always
      type: int
      sample: 1
    name:
      description: The id of the notification.
      returned: always
      type: str
      sample: My Telegram Alert (1)
    active:
      description: 
      returned: always
      type: bool
      sample: True
    user_id:
      description: 
      returned: always
      sample: 1
    default:
      description: 
      returned: always
      type: bool
      sample: False
    type:
      description: 
      returned: always
      type: str
      sample: telegram
    alerta_api_endpoint:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    alerta_api_key:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    alerta_environment:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    alerta_alert_state:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    alerta_recover_state:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    aliyun_sms_phonenumber:
      description: aliyun_sms provider option.
      returned: if type is aliyun_sms
      type: str
    aliyun_sms_template_code:
      description: aliyun_sms provider option.
      returned: if type is aliyun_sms
      type: str
    aliyun_sms_sign_name:
      description: aliyun_sms provider option.
      returned: if type is aliyun_sms
      type: str
    aliyun_sms_access_key_id:
      description: aliyun_sms provider option.
      returned: if type is aliyun_sms
      type: str
    aliyun_sms_secret_access_key:
      description: aliyun_sms provider option.
      returned: if type is aliyun_sms
      type: str
    apprise_url:
      description: apprise provider option.
      returned: if type is apprise
      type: str
    apprise_title:
      description: apprise provider option.
      returned: if type is apprise
      type: str
    bark_endpoint:
      description: bark provider option.
      returned: if type is bark
      type: str
    clicksendsms_login:
      description: clicksendsms provider option.
      returned: if type is clicksendsms
      type: str
    clicksendsms_password:
      description: clicksendsms provider option.
      returned: if type is clicksendsms
      type: str
    clicksendsms_to_number:
      description: clicksendsms provider option.
      returned: if type is clicksendsms
      type: str
    clicksendsms_sender_name:
      description: clicksendsms provider option.
      returned: if type is clicksendsms
      type: str
    ding_ding_web_hook_url:
      description: ding_ding provider option.
      returned: if type is ding_ding
      type: str
    ding_ding_secret_key:
      description: ding_ding provider option.
      returned: if type is ding_ding
      type: str
    discord_username:
      description: discord provider option.
      returned: if type is discord
      type: str
    discord_webhook_url:
      description: discord provider option.
      returned: if type is discord
      type: str
    discord_prefix_message:
      description: discord provider option.
      returned: if type is discord
      type: str
    feishu_web_hook_url:
      description: feishu provider option.
      returned: if type is feishu
      type: str
    google_chat_chat_webhook_url:
      description: google_chat provider option.
      returned: if type is google_chat
      type: str
    gorush_device_token:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorush_platform:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorush_title:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorush_priority:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorush_retry:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorush_topic:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorush_server_url:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gotify_serverurl:
      description: gotify provider option.
      returned: if type is gotify
      type: str
    gotify_application_token:
      description: gotify provider option.
      returned: if type is gotify
      type: str
    gotify_priority:
      description: gotify provider option.
      returned: if type is gotify
      type: str
    line_channel_access_token:
      description: line provider option.
      returned: if type is line
      type: str
    line_user_id:
      description: line provider option.
      returned: if type is line
      type: str
    lunasea_device:
      description: lunasea provider option.
      returned: if type is lunasea
      type: str
    matrix_internal_room_id:
      description: matrix provider option.
      returned: if type is matrix
      type: str
    matrix_access_token:
      description: matrix provider option.
      returned: if type is matrix
      type: str
    matrix_homeserver_url:
      description: matrix provider option.
      returned: if type is matrix
      type: str
    mattermost_username:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    mattermost_webhook_url:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    mattermost_channel:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    mattermost_iconemo:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    mattermost_iconurl:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    ntfy_serverurl:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    ntfy_topic:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    ntfy_priority:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    octopush_version:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_apikey:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_login:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_phone_number:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_smstype:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_sender_name:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_dmlogin:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_dmapikey:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_dmphone_number:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_dmsender_name:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopush_dmsmstype:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    one_bot_http_addr:
      description: one_bot provider option.
      returned: if type is one_bot
      type: str
    one_bot_access_token:
      description: one_bot provider option.
      returned: if type is one_bot
      type: str
    one_bot_msg_type:
      description: one_bot provider option.
      returned: if type is one_bot
      type: str
    one_bot_reciever_id:
      description: one_bot provider option.
      returned: if type is one_bot
      type: str
    pager_duty_duty_auto_resolve:
      description: pager_duty provider option.
      returned: if type is pager_duty
      type: str
    pager_duty_duty_integration_url:
      description: pager_duty provider option.
      returned: if type is pager_duty
      type: str
    pager_duty_duty_priority:
      description: pager_duty provider option.
      returned: if type is pager_duty
      type: str
    pager_duty_duty_integration_key:
      description: pager_duty provider option.
      returned: if type is pager_duty
      type: str
    promosms_login:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    promosms_password:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    promosms_phone_number:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    promosms_smstype:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    promosms_sender_name:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    pushbullet_access_token:
      description: pushbullet provider option.
      returned: if type is pushbullet
      type: str
    push_deer_deer_key:
      description: push_deer provider option.
      returned: if type is push_deer
      type: str
    pushover_userkey:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushover_apptoken:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushover_sounds:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushover_priority:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushover_title:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushover_device:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushy_apikey:
      description: pushy provider option.
      returned: if type is pushy
      type: str
    pushy_token:
      description: pushy provider option.
      returned: if type is pushy
      type: str
    rocket_chat_channel:
      description: rocket_chat provider option.
      returned: if type is rocket_chat
      type: str
    rocket_chat_username:
      description: rocket_chat provider option.
      returned: if type is rocket_chat
      type: str
    rocket_chat_iconemo:
      description: rocket_chat provider option.
      returned: if type is rocket_chat
      type: str
    rocket_chat_webhook_url:
      description: rocket_chat provider option.
      returned: if type is rocket_chat
      type: str
    rocket_chat_button:
      description: rocket_chat provider option.
      returned: if type is rocket_chat
      type: str
    serwersms_username:
      description: serwersms provider option.
      returned: if type is serwersms
      type: str
    serwersms_password:
      description: serwersms provider option.
      returned: if type is serwersms
      type: str
    serwersms_phone_number:
      description: serwersms provider option.
      returned: if type is serwersms
      type: str
    serwersms_sender_name:
      description: serwersms provider option.
      returned: if type is serwersms
      type: str
    signal_number:
      description: signal provider option.
      returned: if type is signal
      type: str
    signal_recipients:
      description: signal provider option.
      returned: if type is signal
      type: str
    signal_url:
      description: signal provider option.
      returned: if type is signal
      type: str
    slack_button:
      description: slack provider option.
      returned: if type is slack
      type: str
    slack_channel:
      description: slack provider option.
      returned: if type is slack
      type: str
    slack_username:
      description: slack provider option.
      returned: if type is slack
      type: str
    slack_iconemo:
      description: slack provider option.
      returned: if type is slack
      type: str
    slack_webhook_url:
      description: slack provider option.
      returned: if type is slack
      type: str
    slack_button:
      description: slack provider option.
      returned: if type is slack
      type: str
    smtp_host:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_port:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_secure:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_ignore_tlserror:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_dkim_domain:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_dkim_key_selector:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_dkim_private_key:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_dkim_hash_algo:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_dkimheader_field_names:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_dkimskip_fields:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_username:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_password:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_custom_subject:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_from:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_cc:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_bcc:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtp_to:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    stackfield_webhook_url:
      description: stackfield provider option.
      returned: if type is stackfield
      type: str
    teams_webhook_url:
      description: teams provider option.
      returned: if type is teams
      type: str
    push_by_techulus_apikey:
      description: push_by_techulus provider option.
      returned: if type is push_by_techulus
      type: str
    telegram_bot_token:
      description: telegram provider option.
      returned: if type is telegram
      type: str
    telegram_chat_id:
      description: telegram provider option.
      returned: if type is telegram
      type: str
    webhook_content_type:
      description: webhook provider option.
      returned: if type is webhook
      type: str
    webhook_url:
      description: webhook provider option.
      returned: if type is webhook
      type: str
    we_com_com_bot_key:
      description: we_com provider option.
      returned: if type is we_com
      type: str
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_notification_by_name
from ansible.module_utils.basic import missing_required_lib

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    if params["id"]:
        notification = api.get_notification(params["id"])
        notifications = [notification]
    elif params["name"]:
        notification = get_notification_by_name(api, params["name"])
        notifications = [notification]
    else:
        notifications = api.get_notifications()

    for notification in notifications:
        # type_ -> type
        notification["type"] = notification.pop("type_")

    result["notifications"] = notifications


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args, supports_check_mode=True)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
    api_token = params.get("api_token")
    if api_token:
      api.login_by_token(api_token)
    else:
      api.login(params["api_username"], params["api_password"])

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
