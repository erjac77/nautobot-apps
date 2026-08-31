from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab


menu_items = (
    NavMenuTab(
        name="Calendars",
        icon="nautobot_calendars/icons/calendar.svg",
        groups=(
            NavMenuGroup(
                name="Calendars",
                weight=100,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_calendars:calendar_list",
                        name="Calendars",
                        permissions=["nautobot_calendars.view_calendar"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_calendars:calendar_add",
                                permissions=["nautobot_calendars.add_calendar"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_calendars:event_list",
                        name="Events",
                        permissions=["nautobot_calendars.view_event"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_calendars:event_add",
                                permissions=["nautobot_calendars.add_event"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_calendars:recurrencerule_list",
                        name="Recurrence Rules",
                        permissions=["nautobot_calendars.view_recurrencerule"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_calendars:recurrencerule_add",
                                permissions=["nautobot_calendars.add_recurrencerule"],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Calendar Types",
                weight=200,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_calendars:calendartype_list",
                        name="Calendar Types",
                        permissions=["nautobot_calendars.view_calendartype"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_calendars:calendartype_add",
                                permissions=["nautobot_calendars.add_calendartype"],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
)
