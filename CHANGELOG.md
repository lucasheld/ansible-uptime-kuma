## Changelog

### Release 1.2.0

#### Features
- add support for uptime kuma 1.23.0 and 1.23.1
- support sendUrl in status_page monitorList (Thanks @obfusk)

#### Bugfixes
- fix proxy retrieval (Thanks @TheLastProject)
- fix maintenances with multiple monitors or status pages
- fix failing status_page test (Thanks @Javex)

### Release 1.1.0

#### Feature
- add support for uptime kuma 1.22.0 and 1.22.1

### Release 1.0.0

#### Feature
- drop support for Uptime Kuma versions < 1.21.3
- add `api_ssl_verify`, `api_wait_events`, `api_timeout` parameters
- add support for uptime kuma 1.21.3
- publish collection to ansible-galaxy

#### Bugfixes
- adjust notification arguments to uptime-kuma-api changes

#### BREAKING CHANGES
- Python 3.7+ required
- maintenance parameter `timezone` renamed to `timezoneOption`
- Removed the `api_wait_timeout` parameter. Use the new `api_timeout` parameter instead. The `api_timeout` parameter specifies how many seconds the client should wait for the connection, an expected event or a server response.
- Uptime Kuma versions < 1.21.3 are not supported in ansible-uptime-kuma 1.0.0+

### Release 0.14.0

#### Feature
- add support for uptime kuma 1.21.2
- add support for args `wait_timeout` and `headers`

### Release 0.13.0

#### Feature
- add support for uptime kuma 1.21.1

#### Bugfix
- add missing mtls authMethod

### Release 0.12.0

#### Feature
- add support for uptime kuma 1.21.0

### Release 0.11.0

#### Feature
- add support for uptime kuma 1.20.0

#### Bugfix
- fix creation of mysql monitor

### Release 0.10.0

#### Feature
- add support for uptime kuma 1.19.5

### Release 0.9.0

#### Feature
- support login with 2fa enabled

### Release 0.8.2

#### Bugfix
- fix ImportError in maintenance module

### Release 0.8.1

#### Bugfix
- monitor tag value is not required

### Release 0.8.0

#### Feature
- support for uptime kuma 1.19.3

### Release 0.7.0

#### Feature
- support for uptime kuma 1.19.2

### Release 0.6.1

#### Bugfix
- comparison of two lists with different length

### Release 0.6.0

#### Feature
- add settings and settings_info module

### Release 0.5.1

#### Bugfix
- use notification provider options types

### Release 0.5.0

#### Feature
- support for uptime kuma 1.18.3

### Release 0.4.0

#### Feature
- support for uptime kuma 1.18.1 / 1.18.2

### Release 0.3.0

#### Feature
- support autoLogin for enabled disableAuth

#### Bugfix
- idempotence for status page with publicGroupList

### Release 0.2.1

#### Bugfix
- adjust to monitor notificationIDList return value

### Release 0.2.0

#### Feature
- support for uptime kuma 1.18.0

#### Bugfix
- rename notification key default to isDefault
- add notification key applyExisting

### Release 0.1.1

#### Bugfix
- allow to add monitors to status pages

### Release 0.1.0

- initial release
