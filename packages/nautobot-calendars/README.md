# Nautobot Calendars App

## Overview

A calendaring/scheduling app for [Nautobot](https://github.com/nautobot/nautobot). It can be used (but not limited to) to define and assign maintenance or blackout schedules to an object (ex: Device). It uses a subset of [RFC 5545](https://datatracker.ietf.org/doc/html/rfc5545) for specifying recurring date/times.

_Nautobot Calendars_ relies on these libraries:

- The `rrule` module of [dateutil](https://dateutil.readthedocs.io/en/stable/rrule.html) as the implementation of the recurrence rules.
- [FullCalendar](https://fullcalendar.io) to display event calendars in the [Nautobot UI](https://docs.nautobot.com/projects/core/en/stable/development/core/ui-component-framework/).

## Concepts

Calendars (or schedules) are rules that include or exclude time for various actions or tasks. They can be used to specify maintenance or blackout windows, service level agreements or inactivity monitors, or on-call rotations.

### Calendar type

A calendar type describes the purpose of the schedule. There are two pre-built types:

- _Maintenance Window_: A pre-scheduled, time-boxed period during which technical staff perform system updates, hardware repairs, or infrastructure maintenance.
- _Blackout Window_: A defined period where system changes, updates, or maintenance are strictly prohibited.

### Calendar

A calendar is a collection of related events, along with additional metadata such as name and description.

### Events

An event is an object associated with a specific date or time range. Besides a start and end date-time, events contain other data such as title, description, organizer, etc. Nautobot Calendar supports single and recurring events:

- A single event represents a unique occurrence.
- A recurring event defines multiple occurrences.

### Recurrence rule

A recurrence rule contains fields representing one or several `RRULE` properties as defined in __RFC 5545__.

The `RRULE` property is the most important as it defines a regular rule for repeating the event. It is composed of the following components:

- `FREQ`: The frequency with which the event should be repeated (such as `DAILY` or `WEEKLY`). Required.
- `UNTIL`: The date or date-time until which the event should be repeated (inclusive).
- `COUNT`: Number of times this event should be repeated.
    You can use either `COUNT` or `UNTIL` to specify the end of the event recurrence. Don't use both in the same rule.
- `INTERVAL`: Works together with `FREQ` to specify how often the event should be repeated. For example, `FREQ=DAILY;INTERVAL=2` means once every two days.
- `BYDAY`: Days of the week on which the event should be repeated (`SU`, `MO`, `TU`, etc.). Other similar components include `BYSECOND`, `BYMINUTE`, `BYHOUR`, `BYMONTHDAY`, `BYYEARDAY`, `BYWEEKNO`, `BYMONTH` and `BYSETPOS`.
- `WKST`: The day on which the workweek starts. Valid values are `MO`, `TU`, `WE`, `TH`, `FR`, `SA`, and `SU`.

## Screenshots

![Navigation](https://raw.githubusercontent.com/erjac77/nautobot-apps/main/docs/assets/images/calendar-navigation.png)

![Calendar](https://raw.githubusercontent.com/erjac77/nautobot-apps/main/docs/assets/images/calendar.png)

![Recurrence Rule](https://raw.githubusercontent.com/erjac77/nautobot-apps/main/docs/assets/images/calendar-recurrence-rule.png)
