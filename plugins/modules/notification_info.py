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

module: notification_info
author: Lucas Held (@lucasheld)
short_description: Retrieves facts about notifications.
description: Retrieves facts about notifications.

options:
  id:
    description:
      - The id of the notification to inspect.
      - Only required if no I(name) specified.
    type: int
  name:
    description:
      - The name of the notification to inspect.
      - Only required if no I(id) specified.
    type: str
'''

EXAMPLES = r'''
- name: get all notifications
  lucasheld.uptime_kuma.notification_info:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
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
    userId:
      description: 
      returned: always
      sample: 1
    isDefault:
      description: True if the notification is the default.
      returned: always
      type: bool
      sample: False
    applyExisting:
      description: True if the notification is applied to all existing monitors.
      returned: always
      type: bool
    type:
      description: 
      returned: always
      type: str
      sample: telegram
    alertaApiEndpoint:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    alertaApiKey:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    alertaEnvironment:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    alertaAlertState:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    alertaRecoverState:
      description: alerta provider option.
      returned: if type is alerta
      type: str
    alertNowWebhookURL:
      description: AlertNow provider option.
      returned: if type is AlertNow
      type: str
    phonenumber:
      description: AliyunSMS provider option.
      returned: if type is AliyunSMS
      type: str
    templateCode:
      description: AliyunSMS provider option.
      returned: if type is AliyunSMS
      type: str
    signName:
      description: AliyunSMS provider option.
      returned: if type is AliyunSMS
      type: str
    accessKeyId:
      description: AliyunSMS provider option.
      returned: if type is AliyunSMS
      type: str
    secretAccessKey:
      description: AliyunSMS provider option.
      returned: if type is AliyunSMS
      type: str
    appriseURL:
      description: apprise provider option.
      returned: if type is apprise
      type: str
    title:
      description: apprise provider option.
      returned: if type is apprise
      type: str
    barkEndpoint:
      description: Bark provider option.
      returned: if type is Bark
      type: str
    barkGroup:
      description: Bark provider option.
      returned: if type is Bark
      type: str
    barkSound:
      description: Bark provider option.
      returned: if type is Bark
      type: str
    clicksendsmsLogin:
      description: clicksendsms provider option.
      returned: if type is clicksendsms
      type: str
    clicksendsmsPassword:
      description: clicksendsms provider option.
      returned: if type is clicksendsms
      type: str
    clicksendsmsToNumber:
      description: clicksendsms provider option.
      returned: if type is clicksendsms
      type: str
    clicksendsmsSenderName:
      description: clicksendsms provider option.
      returned: if type is clicksendsms
      type: str
    webHookUrl:
      description: DingDing provider option.
      returned: if type is DingDing
      type: str
    secretKey:
      description: DingDing provider option.
      returned: if type is DingDing
      type: str
    discordUsername:
      description: discord provider option.
      returned: if type is discord
      type: str
    discordWebhookUrl:
      description: discord provider option.
      returned: if type is discord
      type: str
    discordPrefixMessage:
      description: discord provider option.
      returned: if type is discord
      type: str
    feishuWebHookUrl:
      description: Feishu provider option.
      returned: if type is Feishu
      type: str
    flashdutySeverity:
      description: FlashDuty provider option.
      returned: if type is FlashDuty
      type: str
    flashdutyIntegrationKey:
      description: FlashDuty provider option.
      returned: if type is FlashDuty
      type: str
    freemobileUser:
      description: FreeMobile provider option.
      returned: if type is FreeMobile
      type: str
    freemobilePass:
      description: FreeMobile provider option.
      returned: if type is FreeMobile
      type: str
    goAlertBaseURL:
      description: GoAlert provider option.
      returned: if type is GoAlert
      type: str
    goAlertToken:
      description: GoAlert provider option.
      returned: if type is GoAlert
      type: str
    googleChatWebhookURL:
      description: GoogleChat provider option.
      returned: if type is GoogleChat
      type: str
    gorushDeviceToken:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorushPlatform:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorushTitle:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorushPriority:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorushRetry:
      description: gorush provider option.
      returned: if type is gorush
      type: int
    gorushTopic:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gorushServerURL:
      description: gorush provider option.
      returned: if type is gorush
      type: str
    gotifyserverurl:
      description: gotify provider option.
      returned: if type is gotify
      type: str
    gotifyapplicationToken:
      description: gotify provider option.
      returned: if type is gotify
      type: str
    gotifyPriority:
      description: gotify provider option.
      returned: if type is gotify
      type: int
    notificationService:
      description: HomeAssistant provider option.
      returned: if type is HomeAssistant
      type: str
    homeAssistantUrl:
      description: HomeAssistant provider option.
      returned: if type is HomeAssistant
      type: str
    longLivedAccessToken:
      description: HomeAssistant provider option.
      returned: if type is HomeAssistant
      type: str
    kookGuildID:
      description: Kook provider option.
      returned: if type is Kook
      type: str
    kookBotToken:
      description: Kook provider option.
      returned: if type is Kook
      type: str
    lineChannelAccessToken:
      description: line provider option.
      returned: if type is line
      type: str
    lineUserID:
      description: line provider option.
      returned: if type is line
      type: str
    lineNotifyAccessToken:
      description: LineNotify provider option.
      returned: if type is LineNotify
      type: str
    lunaseaTarget:
      description: lunasea provider option.
      returned: if type is lunasea
      type: str
    lunaseaUserID:
      description: lunasea provider option.
      returned: if type is lunasea
      type: str
    lunaseaDevice:
      description: lunasea provider option.
      returned: if type is lunasea
      type: str
    internalRoomId:
      description: matrix provider option.
      returned: if type is matrix
      type: str
    accessToken:
      description: matrix provider option.
      returned: if type is matrix
      type: str
    homeserverUrl:
      description: matrix provider option.
      returned: if type is matrix
      type: str
    mattermostusername:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    mattermostWebhookUrl:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    mattermostchannel:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    mattermosticonemo:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    mattermosticonurl:
      description: mattermost provider option.
      returned: if type is mattermost
      type: str
    sender:
      description: nostr provider option.
      returned: if type is nostr
      type: str
    recipients:
      description: nostr provider option.
      returned: if type is nostr
      type: str
    relays:
      description: nostr provider option.
      returned: if type is nostr
      type: str
    ntfyAuthenticationMethod:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    ntfyusername:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    ntfypassword:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    ntfyaccesstoken:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    ntfytopic:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    ntfyPriority:
      description: ntfy provider option.
      returned: if type is ntfy
      type: int
    ntfyserverurl:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    ntfyIcon:
      description: ntfy provider option.
      returned: if type is ntfy
      type: str
    octopushVersion:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopushAPIKey:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopushLogin:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopushPhoneNumber:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopushSMSType:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    octopushSenderName:
      description: octopush provider option.
      returned: if type is octopush
      type: str
    httpAddr:
      description: OneBot provider option.
      returned: if type is OneBot
      type: str
    accessToken:
      description: OneBot provider option.
      returned: if type is OneBot
      type: str
    msgType:
      description: OneBot provider option.
      returned: if type is OneBot
      type: str
    recieverId:
      description: OneBot provider option.
      returned: if type is OneBot
      type: str
    opsgeniePriority:
      description: Opsgenie provider option.
      returned: if type is Opsgenie
      type: int
    opsgenieRegion:
      description: Opsgenie provider option.
      returned: if type is Opsgenie
      type: str
    opsgenieApiKey:
      description: Opsgenie provider option.
      returned: if type is Opsgenie
      type: str
    pagerdutyAutoResolve:
      description: PagerDuty provider option.
      returned: if type is PagerDuty
      type: str
    pagerdutyIntegrationUrl:
      description: PagerDuty provider option.
      returned: if type is PagerDuty
      type: str
    pagerdutyPriority:
      description: PagerDuty provider option.
      returned: if type is PagerDuty
      type: str
    pagerdutyIntegrationKey:
      description: PagerDuty provider option.
      returned: if type is PagerDuty
      type: str
    pagertreeAutoResolve:
      description: PagerTree provider option.
      returned: if type is PagerTree
      type: str
    pagertreeIntegrationUrl:
      description: PagerTree provider option.
      returned: if type is PagerTree
      type: str
    pagertreeUrgency:
      description: PagerTree provider option.
      returned: if type is PagerTree
      type: str
    promosmsAllowLongSMS:
      description: promosms provider option.
      returned: if type is promosms
      type: bool
    promosmsLogin:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    promosmsPassword:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    promosmsPhoneNumber:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    promosmsSMSType:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    promosmsSenderName:
      description: promosms provider option.
      returned: if type is promosms
      type: str
    pushbulletAccessToken:
      description: pushbullet provider option.
      returned: if type is pushbullet
      type: str
    pushdeerServer:
      description: PushDeer provider option.
      returned: if type is PushDeer
      type: str
    pushdeerKey:
      description: PushDeer provider option.
      returned: if type is PushDeer
      type: str
    pushoveruserkey:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushoverapptoken:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushoversounds:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushoverpriority:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushovertitle:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushoverdevice:
      description: pushover provider option.
      returned: if type is pushover
      type: str
    pushoverttl:
      description: pushover provider option.
      returned: if type is pushover
      type: int
    pushyAPIKey:
      description: pushy provider option.
      returned: if type is pushy
      type: str
    pushyToken:
      description: pushy provider option.
      returned: if type is pushy
      type: str
    rocketchannel:
      description: rocket.chat provider option.
      returned: if type is rocket.chat
      type: str
    rocketusername:
      description: rocket.chat provider option.
      returned: if type is rocket.chat
      type: str
    rocketiconemo:
      description: rocket.chat provider option.
      returned: if type is rocket.chat
      type: str
    rocketwebhookURL:
      description: rocket.chat provider option.
      returned: if type is rocket.chat
      type: str
    serverChanSendKey:
      description: ServerChan provider option.
      returned: if type is ServerChan
      type: str
    serwersmsUsername:
      description: serwersms provider option.
      returned: if type is serwersms
      type: str
    serwersmsPassword:
      description: serwersms provider option.
      returned: if type is serwersms
      type: str
    serwersmsPhoneNumber:
      description: serwersms provider option.
      returned: if type is serwersms
      type: str
    serwersmsSenderName:
      description: serwersms provider option.
      returned: if type is serwersms
      type: str
    signalNumber:
      description: signal provider option.
      returned: if type is signal
      type: str
    signalRecipients:
      description: signal provider option.
      returned: if type is signal
      type: str
    signalURL:
      description: signal provider option.
      returned: if type is signal
      type: str
    slackchannelnotify:
      description: slack provider option.
      returned: if type is slack
      type: bool
    slackchannel:
      description: slack provider option.
      returned: if type is slack
      type: str
    slackusername:
      description: slack provider option.
      returned: if type is slack
      type: str
    slackiconemo:
      description: slack provider option.
      returned: if type is slack
      type: str
    slackwebhookURL:
      description: slack provider option.
      returned: if type is slack
      type: str
    smscTranslit:
      description: smsc provider option.
      returned: if type is smsc
      type: str
    smscLogin:
      description: smsc provider option.
      returned: if type is smsc
      type: str
    smscPassword:
      description: smsc provider option.
      returned: if type is smsc
      type: str
    smscToNumber:
      description: smsc provider option.
      returned: if type is smsc
      type: str
    smscSenderName:
      description: smsc provider option.
      returned: if type is smsc
      type: str
    smseagleEncoding:
      description: SMSEagle provider option.
      returned: if type is SMSEagle
      type: bool
    smseaglePriority:
      description: SMSEagle provider option.
      returned: if type is SMSEagle
      type: int
    smseagleRecipientType:
      description: SMSEagle provider option.
      returned: if type is SMSEagle
      type: str
    smseagleToken:
      description: SMSEagle provider option.
      returned: if type is SMSEagle
      type: str
    smseagleRecipient:
      description: SMSEagle provider option.
      returned: if type is SMSEagle
      type: str
    smseagleUrl:
      description: SMSEagle provider option.
      returned: if type is SMSEagle
      type: str
    smsmanagerApiKey:
      description: SMSManager provider option.
      returned: if type is SMSManager
      type: str
    numbers:
      description: SMSManager provider option.
      returned: if type is SMSManager
      type: str
    messageType:
      description: SMSManager provider option.
      returned: if type is SMSManager
      type: str
    smtpHost:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpPort:
      description: smtp provider option.
      returned: if type is smtp
      type: int
    smtpSecure:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpIgnoreTLSError:
      description: smtp provider option.
      returned: if type is smtp
      type: bool
    smtpDkimDomain:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpDkimKeySelector:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpDkimPrivateKey:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpDkimHashAlgo:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpDkimheaderFieldNames:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpDkimskipFields:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpUsername:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpPassword:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    customSubject:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpFrom:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpCC:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpBCC:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    smtpTo:
      description: smtp provider option.
      returned: if type is smtp
      type: str
    splunkAutoResolve:
      description: Splunk provider option.
      returned: if type is Splunk
      type: str
    splunkSeverity:
      description: Splunk provider option.
      returned: if type is Splunk
      type: str
    splunkRestURL:
      description: Splunk provider option.
      returned: if type is Splunk
      type: str
    squadcastWebhookURL:
      description: squadcast provider option.
      returned: if type is squadcast
      type: str
    stackfieldwebhookURL:
      description: stackfield provider option.
      returned: if type is stackfield
      type: str
    webhookUrl:
      description: teams provider option.
      returned: if type is teams
      type: str
    pushAPIKey:
      description: PushByTechulus provider option.
      returned: if type is PushByTechulus
      type: str
    telegramChatID:
      description: telegram provider option.
      returned: if type is telegram
      type: str
    telegramSendSilently:
      description: telegram provider option.
      returned: if type is telegram
      type: bool
    telegramProtectContent:
      description: telegram provider option.
      returned: if type is telegram
      type: bool
    telegramMessageThreadID:
      description: telegram provider option.
      returned: if type is telegram
      type: str
    telegramBotToken:
      description: telegram provider option.
      returned: if type is telegram
      type: str
    twilioAccountSID:
      description: twilio provider option.
      returned: if type is twilio
      type: str
    twilioApiKey:
      description: twilio provider option.
      returned: if type is twilio
      type: str
    twilioAuthToken:
      description: twilio provider option.
      returned: if type is twilio
      type: str
    twilioToNumber:
      description: twilio provider option.
      returned: if type is twilio
      type: str
    twilioFromNumber:
      description: twilio provider option.
      returned: if type is twilio
      type: str
    webhookContentType:
      description: webhook provider option.
      returned: if type is webhook
      type: str
    webhookCustomBody:
      description: webhook provider option.
      returned: if type is webhook
      type: str
    webhookAdditionalHeaders:
      description: webhook provider option.
      returned: if type is webhook
      type: str
    webhookURL:
      description: webhook provider option.
      returned: if type is webhook
      type: str
    weComBotKey:
      description: WeCom provider option.
      returned: if type is WeCom
      type: str
    webhookUrl:
      description: ZohoCliq provider option.
      returned: if type is ZohoCliq
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
