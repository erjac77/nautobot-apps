---
icon: lucide/blocks
---

# Nautobot Apps

## Overview

The _Nautobot Apps_ is a collection of community-developed [Nautobot] applications, released under the [MIT license](https://opensource.org/license/MIT) and hosted on a single repository [GitHub](https://github.com/erjac77/nautobot-apps) ([monorepo](https://monorepo.tools)).

[Nautobot] is an open source Network Source of Truth and Automation Platform built to help network teams unify data, model intended state, and execute automation with confidence.

Apps (or plugins) are packaged Django apps that can be installed alongside [Nautobot] to provide custom functionality not present in the core application. Plugins can introduce their own models and views, but cannot interfere with existing components.

!!! note

    Throughout this documentation, the terms "app" and "plugin" will be used interchangeably.

## Apps

|                                                                                                                                              | Name                                     | Description                                                                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Calendar](assets/icons/calendar-light.svg#only-light){ width="100%" }![Calendar](assets/icons/calendar-dark.svg#only-dark){ width="100%" } | [Nautobot Calendars](calendars/index.md) | A calendaring/scheduling application for [Nautobot]. It can be used to define and assign maintenance or blackout schedules to an object (ex: Device). It uses a subset of [RFC 5545](https://datatracker.ietf.org/doc/html/rfc5545) (wraps `dateutil.rrule`) for specifying recurring date/times. |

[Nautobot]: https://github.com/nautobot/nautobot
