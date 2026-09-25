from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab


menu_items = (
    NavMenuTab(
        name="Schedules",
        icon="nautobot_schedule/icons/calendar.svg",
        groups=(
            NavMenuGroup(
                name="Schedules",
                weight=100,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_schedule:schedule_list",
                        name="Schedules",
                        permissions=["nautobot_schedule.view_schedule"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_schedule:schedule_add",
                                permissions=["nautobot_schedule.add_schedule"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_schedule:event_list",
                        name="Events",
                        permissions=["nautobot_schedule.view_event"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_schedule:event_add",
                                permissions=["nautobot_schedule.add_event"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_schedule:recurrencerule_list",
                        name="Recurrence Rules",
                        permissions=["nautobot_schedule.view_recurrencerule"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_schedule:recurrencerule_add",
                                permissions=["nautobot_schedule.add_recurrencerule"],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Schedule Types",
                weight=200,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_schedule:scheduletype_list",
                        name="Schedule Types",
                        permissions=["nautobot_schedule.view_scheduletype"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_schedule:scheduletype_add",
                                permissions=["nautobot_schedule.add_scheduletype"],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
)
