from django.contrib import admin
from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from tickets.views import (
    TicketViewSet,
    NamespaceViewSet,
    SingleTicketViewSet
)

from status.views import StatusViewSet

ticket_router = DefaultRouter()
ticket_router.register(r'', TicketViewSet)

simple_ticket_router = DefaultRouter()
simple_ticket_router.register(r'', SingleTicketViewSet)

namespace_router = DefaultRouter()
namespace_router.register(r'', NamespaceViewSet)

status_router = DefaultRouter()
status_router.register(r'', StatusViewSet, basename='status_view_set')

# swagger documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Tickets API Documentation",
      default_version=getattr(settings, 'VERSION', None),
      description="** API Documentation **",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('', include('slack.urls')),
    path('tickets/', include(ticket_router.urls)),
    path('simple/', include(simple_ticket_router.urls)),
    path('namespace/', include(namespace_router.urls)),
    path('status/', include(status_router.urls)),
]
