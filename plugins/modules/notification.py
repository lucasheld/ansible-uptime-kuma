#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
extends_documentation_fragment:
  - lucasheld.uptime_kuma.uptime_kuma

module: notification
author: Lucas Held (@lucasheld)
short_description: Manages notifications.
description: Manages notifications. All properties described in the [python module docs](https://uptime-kuma-api.readthedocs.io/en/latest/api.html#uptime_kuma_api.UptimeKumaApi.edit_notification) are allowed as args.

options:
  id:
    description:
      - The id of the notification.
      - Only required if no I(name) specified.
    type: int
  name:
    description:
      - The name of the notification.
      - Only required if no I(id) specified.
    type: str
  isDefault:
    description: True if the notification is the default.
    type: bool
  applyExisting:
    description: True if the notification is applied to all existing monitors.
    type: bool
  state:
    description:
      - Set to C(present) to create/update a notification.
      - Set to C(absent) to delete a notification.
    type: str
    default: present
    choices: ["present", "absent"]
'''

EXAMPLES = r'''
- name: Add notification
  lucasheld.uptime_kuma.notification:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Notification 1
    type: telegram
    isDefault: false
    applyExisting: false
    telegramBotToken: 1111
    telegramChatID: 2222
    state: present

- name: Edit notification
  lucasheld.uptime_kuma.notification:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Notification 1
    type: telegram
    isDefault: false
    applyExisting: false
    telegramBotToken: 6666
    telegramChatID: 7777
    state: present

- name: Remove notification
  lucasheld.uptime_kuma.notification:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Notification 1
    state: absent
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import object_changed, clear_params, common_module_args, get_notification_by_name, \
    clear_unset_params

try:
    from uptime_kuma_api import UptimeKumaApi, notification_provider_options

    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def build_provider_args():
    provider_args = {}
    for provider_options in notification_provider_options.values():
        if type(provider_options) == list:  # backward compatible
            provider_options = {option: dict(type="str") for option in provider_options}
        for option, args in provider_options.items():
            if "password" in option.lower():
                args["no_log"] = True
            provider_args[option] = {
                "type": args["type"]
            }
    return provider_args


def build_providers():
    providers = []
    for provider_enum in notification_provider_options:
        provider = provider_enum.__dict__["_value_"]
        providers.append(provider)
    return providers


def build_provider_options():
    options = []
    for provider_options in notification_provider_options.values():
        options.extend(provider_options)
    return options


def run(api, params, result):
    state = params["state"]
    options = clear_params(params)
    options = clear_unset_params(options)

    if params["id"]:
        notification = api.get_notification(params["id"])
    else:
        notification = get_notification_by_name(api, params["name"])

    if state == "present":
        if not notification:
            api.add_notification(**options)
            result["changed"] = True
        else:
            changed_keys = object_changed(notification, options)
            if changed_keys:
                api.edit_notification(notification["id"], **options)
                result["changed"] = True
    elif state == "absent":
        if notification:
            api.delete_notification(notification["id"])
            result["changed"] = True


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
        isDefault=dict(type="bool", aliases=["default"]),
        applyExisting=dict(type="bool"),
        state=dict(type="str", default="present", choices=["present", "absent"]),

        # Alerta
        alertaApiEndpoint=dict(type="str"),
        alertaApiKey=dict(type="str"),
        alertaAlertState=dict(type="str"),
        alertaRecoverState=dict(type="str"),

        # Alert Now
        alertNowWebhookURL=dict(type="str"),

        # Aliyun SMS
        phonenumber=dict(type="str"),
        templateCode=dict(type="str"),
        signName=dict(type="str"),
        accessKeyId=dict(type="str"),
        secretAccessKey=dict(type="str"),

        # Apprise
        appriseURL=dict(type="str"),
        title=dict(type="str"),

        # Bark
        barkEndpoint=dict(type="str"),
        barkGroup=dict(type="str"),
        barkSound=dict(type="str"),

        # ClicksendSMS
        clicksendsmsLogin=dict(type="str"),
        clicksendsmsPassword=dict(type="str"),
        clicksendsmsToNumber=dict(type="str"),
        clicksendsmsSenderName=dict(type="str"),

        # Dingding
        webHookUrl=dict(type="str"),
        secretKey=dict(type="str"),

        # Discord
        discordUsername=dict(type="str"),
        discordWebhookUrl=dict(type="str"),
        discordPrefixMessage=dict(type="str"),

        # Feishu
        feishuWebHookUrl=dict(type="str"),

        # Flashduty
        flashdutySeverity=dict(type="str"),
        flashdutyIntegrationKey=dict(type="str"),

        # Freemobile
        freemobileUser=dict(type="str"),
        freemobilePass=dict(type="str"),

        # Goalert
        goAlertBaseURL=dict(type="str"),
        goAlertToken=dict(type="str"),

        # Googlechat
        googleChatWebhookURL=dict(type="str"),

        # Gorush
        gorushDeviceToken=dict(type="str"),
        gorushPlatform=dict(type="str"),
        gorushTitle=dict(type="str"),
        gorushPriority=dict(type="str"),
        gorushRetry=dict(type="int"),
        gorushTopic=dict(type="str"),
        gorushServerURL=dict(type="str"),

        # Gotify
        gotifyserverurl=dict(type="str"),
        gotifyapplicationToken=dict(type="str"),
        gotifyPriority=dict(type="int"),

        # Homeassistant
        notificationService=dict(type="str"),
        homeAssistantUrl=dict(type="str"),
        longLivedAccessToken=dict(type="str"),

        # Kook
        kookGuildID=dict(type="str"),
        kookBotToken=dict(type="str"),

        # Line
        lineChannelAccessToken=dict(type="str"),
        lineUserID=dict(type="str"),
        lineNotifyAccessToken=dict(type="str"),

        # Lunasea
        lunaseaTarget=dict(type="str"),
        lunaseaUserID=dict(type="str"),
        lunaseaDevice=dict(type="str"),

        # Matrix
        internalRoomId=dict(type="str"),
        accessToken=dict(type="str"),
        homeserverUrl=dict(type="str"),

        # Mattermost
        mattermostusername=dict(type="str"),
        mattermostWebhookUrl=dict(type="str"),
        mattermostchannel=dict(type="str"),
        mattermosticonemo=dict(type="str"),
        mattermosticonurl=dict(type="str"),

        # Nostr
        sender=dict(type="str"),
        recipients=dict(type="str"),
        relays=dict(type="str"),

        # NTFY
        ntfyAuthenticationMethod=dict(type="str"),
        ntfyusername=dict(type="str"),
        ntfypassword=dict(type="str"),
        ntfyaccesstoken=dict(type="str"),
        ntfytopic=dict(type="str"),
        ntfyPriority=dict(type="int"),
        ntfyserverurl=dict(type="str"),
        ntfyIcon=dict(type="str"),

        # Octopush
        octopushVersion=dict(type="str"),
        octopushAPIKey=dict(type="str"),
        octopushLogin=dict(type="str"),
        octopushPhoneNumber=dict(type="str"),
        octopushSMSType=dict(type="str"),
        octopushSenderName=dict(type="str"),

        # Onebot
        httpAddr=dict(type="str"),
        # Already registered in the Matrix Section
        #accessToken=dict(type="str"),
        msgType=dict(type="str"),
        recieverId=dict(type="str"),

        # Opsgenie
        opsgeniePriority=dict(type="int"),
        opsgenieRegion=dict(type="str"),
        opsgenieApiKey=dict(type="str"),

        # Pagerduty
        pagerdutyAutoResolve=dict(type="str"),
        pagerdutyIntegrationUrl=dict(type="str"),
        pagerdutyPriority=dict(type="str"),
        pagerdutyIntegrationKey=dict(type="str"),

        # Pagertree
        pagertreeAutoResolve=dict(type="str"),
        pagertreeIntegrationUrl=dict(type="str"),
        pagertreeUrgency=dict(type="str"),

         # Promosms
        promosmsAllowLongSMS=dict(type="str"),
        promosmsLogin=dict(type="str"),
        promosmsPassword=dict(type="str"),
        promosmsPhoneNumber=dict(type="str"),
        promosmsSMSType=dict(type="str"),
        promosmsSenderName=dict(type="str"),

        # Pushbullet
        pushbulletAccessToken=dict(type="str"),

        # Pushdeer
        pushdeerServer=dict(type="str"),
        pushdeerKey=dict(type="str"),

        # Pushover
        pushoveruserkey=dict(type="str"),
        pushoverapptoken=dict(type="str"),
        pushoversounds=dict(type="str"),
        pushoverpriority=dict(type="str"),
        pushovertitle=dict(type="str"),
        pushoverdevice=dict(type="str"),
        pushoverttl=dict(type="int"),

        # Pushy
        pushyAPIKey=dict(type="str"),
        pushyToken=dict(type="str"),

        # Rocketchat
        rocketchannel=dict(type="str"),
        rocketusername=dict(type="str"),
        rocketiconemo=dict(type="str"),
        rocketwebhookURL=dict(type="str"),

        # Serverchan
        serverChanSendKey=dict(type="str"),

        # SerwerSMS
        serwersmsUsername=dict(type="str"),
        serwersmsPassword=dict(type="str"),
        serwersmsPhoneNumber=dict(type="str"),
        serwersmsSenderName=dict(type="str"),

        # Signal
        signalNumber=dict(type="str"),
        signalRecipients=dict(type="str"),
        signalURL=dict(type="str"),

        # Slack
        slackchannelnotify=dict(type="str"),
        slackchannel=dict(type="str"),
        slackusername=dict(type="str"),
        slackiconemo=dict(type="str"),
        slackwebhookURL=dict(type="str"),

        # SMSC
        smscTranslit=dict(type="str"),
        smscLogin=dict(type="str"),
        smscPassword=dict(type="str"),
        smscToNumber=dict(type="str"),
        smscSenderName=dict(type="str"),

        # SMSEagle
        smseagleEncoding=dict(type="str"),
        smseaglePriority=dict(type="int"),
        smseagleRecipientType=dict(type="str"),
        smseagleToken=dict(type="str"),
        smseagleRecipient=dict(type="str"),
        smseagleUrl=dict(type="str"),

        # SMS Manager
        smsmanagerApiKey=dict(type="str"),
        numbers=dict(type="str"),
        messageType=dict(type="str"),

        # SMTP
        smtpHost=dict(type="str"),
        smtpPort=dict(type="int"),
        smtpSecure=dict(type="str"),
        smtpIgnoreTLSError=dict(type="str"),
        smtpDkimDomain=dict(type="str"),
        smtpDkimKeySelector=dict(type="str"),
        smtpDkimPrivateKey=dict(type="str"),
        smtpDkimHashAlgo=dict(type="str"),
        smtpDkimheaderFieldNames=dict(type="str"),
        smtpDkimskipFields=dict(type="str"),
        smtpUsername=dict(type="str"),
        smtpPassword=dict(type="str"),
        customSubject=dict(type="str"),
        smtpFrom=dict(type="str"),
        smtpCC=dict(type="str"),
        smtpBCC=dict(type="str"),
        smtpTo=dict(type="str"),

        # Splunk
        splunkAutoResolve=dict(type="str"),
        splunkSeverity=dict(type="str"),
        splunkRestURL=dict(type="str"),

        # Suqadcast
        squadcastWebhookURL=dict(type="str"),

        # Stackfield
        stackfieldwebhookURL=dict(type="str"),

        # Teams
        webhookUrl=dict(type="str"),

        # Pushbyte
        pushAPIKey=dict(type="str"),

        # Telegram
        telegramChatID=dict(type="str"),
        telegramSendSilently=dict(type="str"),
        telegramProtectContent=dict(type="str"),
        telegramMessageThreadID=dict(type="str"),
        telegramBotToken=dict(type="str"),

        # Twilio
        twilioAccountSID=dict(type="str"),
        twilioApiKey=dict(type="str"),
        twilioAuthToken=dict(type="str"),
        twilioToNumber=dict(type="str"),
        twilioFromNumber=dict(type="str"),

        # Webhook
        webhookContentType=dict(type="str"),
        webhookCustomBody=dict(type="str"),
        webhookAdditionalHeaders=dict(type="str"),
        webhookURL=dict(type="str"),

        # Wecom
        weComBotKey=dict(type="str"),

        # Zohocliq
        # Already registered in the Matrix Section
        #webhookUrl=dict(type="str")
    )

    if HAS_UPTIME_KUMA_API:
        provider_types = build_providers()
        module_args.update(type=dict(type="str", choices=provider_types))

        provider_args = build_provider_args()
        module_args.update(provider_args)

    module_args.update(common_module_args)

    module = AnsibleModule(module_args)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"], timeout=params["api_timeout"], headers=params["api_headers"], ssl_verify=params["api_ssl_verify"], wait_events=params["api_wait_events"])
    api_token = params.get("api_token")
    api_username = params.get("api_username")
    api_password = params.get("api_password")
    if api_token:
        api.login_by_token(api_token)
    elif api_username and api_password:
        api.login(api_username, api_password)
    else:
        # autoLogin for enabled disableAuth
        api.login()

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
