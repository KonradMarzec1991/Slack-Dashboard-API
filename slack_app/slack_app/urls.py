from django.contrib import admin
from django.urls import include, path

from tickets.views import (
    TicketViewSet,
    NamespaceViewSet,
    SingleTicketViewSet
)

from status.views import StatusViewSet

from rest_framework.routers import DefaultRouter

ticket_router = DefaultRouter()
ticket_router.register(r'', TicketViewSet)

simple_ticket_router = DefaultRouter()
simple_ticket_router.register(r'', SingleTicketViewSet)

namespace_router = DefaultRouter()
namespace_router.register(r'', NamespaceViewSet)

status_router = DefaultRouter()
status_router.register(r'', StatusViewSet, base_name='status_view_set')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('slack.urls')),
    path('tickets/', include(ticket_router.urls)),
    path('simple/', include(simple_ticket_router.urls)),
    path('namespace/', include(namespace_router.urls)),
    path('status/', include(status_router.urls)),
]