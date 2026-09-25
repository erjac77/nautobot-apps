from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

from nautobot_schedule import app_name, views


router = NautobotUIViewSetRouter()

router.register("schedule-types", views.ScheduleTypeUIViewSet)
router.register("schedules", views.ScheduleUIViewSet)
router.register("recurrence-rules", views.RecurrenceRuleUIViewSet)
router.register("events", views.EventUIViewSet)

urlpatterns = [
    path(
        "schedules/<uuid:pk>/events/add/",
        RedirectView.as_view(
            url="/plugins/schedule/events/add/?schedule=%(pk)s&return_url=/plugins/schedule/schedules/%(pk)s/",
        ),
        name="schedule_event_add",
    ),
    path(
        "docs/",
        RedirectView.as_view(url=static(f"{app_name}/docs/index.html")),
        name="docs",
    ),
]

urlpatterns += router.urls  # ty: ignore[unsupported-operator]
