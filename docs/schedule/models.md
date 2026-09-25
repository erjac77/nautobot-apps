---
icon: lucide/file-box
---

# Data models

## Class diagram

```mermaid
classDiagram
    class ScheduleType {
        +CharField name
        +TextField description
    }

    class Schedule {
        +ForeignKey schedule_type
        +CharField name
        +TextField description
    }

    class RecurrenceRule {
        +CharField name
        +PositiveIntegerField freq
        +PositiveIntegerField interval
        +PositiveIntegerField count
        +DateTimeField until
        +JSONField bysecond
        +JSONField byminute
        +JSONField byhour
        +JSONField byday
        +JSONField bymonthday
        +JSONField byyearday
        +JSONField byweekno
        +JSONField bymonth
        +JSONField bysetpos
        +PositiveIntegerField wkst
    }

    class Event {
        +ForeignKey schedule
        +CharField title
        +TextField description
        +DateTimeField dtstart
        +DateTimeField dtend
        +ForeignKey organizer
        +PositiveIntegerField priority
        +ForeignKey recurrence_rule
        +JSONField exdates
        +JSONField rdates
    }

    ScheduleType "1" --o "0..*" Schedule : schedule
    Schedule "1" --o "0..*" Event : events
    RecurrenceRule "0..1" --o "0..*" Event : events
```
