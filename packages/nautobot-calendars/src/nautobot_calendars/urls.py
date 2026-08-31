from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

from nautobot_calendars import app_name, views


router = NautobotUIViewSetRouter()

router.register("calendars", views.CalendarUIViewSet)
router.register("calendar-types", views.CalendarTypeUIViewSet)
router.register("events", views.EventUIViewSet)
router.register("recurrence-rules", views.RecurrenceRuleUIViewSet)


urlpatterns = [
    path(
        "calendars/<uuid:pk>/events/add/",
        RedirectView.as_view(
            url="/plugins/calendars/events/add/?calendar=%(pk)s&return_url=/plugins/calendars/calendars/%(pk)s/",
        ),
        name="calendar_event_add",
    ),
    path(
        "docs/",
        RedirectView.as_view(url=static(f"{app_name}/docs/apps/calendars/index.html")),
        name="docs",
    ),
]

urlpatterns += router.urls
