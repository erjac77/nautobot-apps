from nautobot.apps.api import OrderedDefaultRouter

from nautobot_schedule.api import views


router = OrderedDefaultRouter()

router.register("schedule-types", views.ScheduleTypeViewSet)
router.register("schedules", views.ScheduleViewSet)
router.register("recurrence-rules", views.RecurrenceRuleViewSet)
router.register("events", views.EventViewSet)

urlpatterns = router.urls
