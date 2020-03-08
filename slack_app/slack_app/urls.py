from django.contrib import admin
from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework_nested import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from tickets.views import (
    TicketViewSet,
    NamespaceViewSet,
    SingleTicketViewSet,
    index
)

from status.views import StatusViewSet

router = DefaultRouter()
router.register(r'simple', SingleTicketViewSet, base_name='simple')
router.register(r'status', StatusViewSet, base_name='status')

namespace_router = DefaultRouter()
namespace_router.register(r'namespaces', NamespaceViewSet)

# nested router for tickets and namespaces
namespace_tickets_router = routers.NestedDefaultRouter(
    namespace_router, r'namespaces', lookup='namespace')
namespace_tickets_router.register(
    r'tickets', TicketViewSet, base_name='tickets_namespaces')

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
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('', include('slack.urls')),
    path('', include(router.urls)),
    path('', include(namespace_router.urls)),
    path('', include(namespace_tickets_router.urls)),
]
