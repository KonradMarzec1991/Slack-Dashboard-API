from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    display_dialog,
    proceed_payload,
    show_my_tickets,
    SlackInformationViewSet,
)

slack_router = DefaultRouter()
slack_router.register('display_information', SlackInformationViewSet, base_name='slack_information')

urlpatterns = [
    path('display_dialog/', display_dialog, name='display_dialog'),
    path('', include(slack_router.urls), name='slack_information'),
    path('proceed_payload/', proceed_payload, name='proceed_payload'),
    path('show_tickets/', show_my_tickets, name='show_tickets'),
]
