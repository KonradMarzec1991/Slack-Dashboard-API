from django.contrib import admin
from django.urls import include, path

from tickets.api import TicketViewSet, NamespaceViewSet

from rest_framework.routers import DefaultRouter

ticket_router = DefaultRouter()
ticket_router.register(r'', TicketViewSet)

namespace_router = DefaultRouter()
namespace_router.register(r'', NamespaceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('slack.urls')),
    path('tickets/', include(ticket_router.urls)),
    path('namespace/', include(namespace_router.urls)),
]
