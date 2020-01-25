from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    display_dialog,
    proceed_payload,
    SlackTicketsListViewSet,
    SlackInformationViewSet,
)

slack_router = DefaultRouter()
slack_router.register('display_information', SlackInformationViewSet, base_name='slack_information')
slack_router.register('show_tickets', SlackTicketsListViewSet, base_name='slack_show_tickets')

urlpatterns = [
    path('display_dialog/', display_dialog, name='display_dialog'),
    path('', include(slack_router.urls), name='slack_information'),
    path('proceed_payload/', proceed_payload, name='proceed_payload'),
]
