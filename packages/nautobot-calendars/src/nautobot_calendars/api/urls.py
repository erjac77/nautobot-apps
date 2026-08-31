from nautobot.apps.api import OrderedDefaultRouter

from nautobot_calendars.api import views


router = OrderedDefaultRouter()
router.register("calendars", views.CalendarViewSet)
router.register("calendar-types", views.CalendarTypeViewSet)
router.register("events", views.EventViewSet)
router.register("recurrence-rules", views.RecurrenceRuleViewSet)

urlpatterns = router.urls
