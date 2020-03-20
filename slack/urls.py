from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SlackDialogViewSet,
    SlackTicketsListViewSet,
    SlackInformationViewSet,
    slack_payload
)

slack_router = DefaultRouter()
slack_router.register('display_information', SlackInformationViewSet,
                      basename='slack_information')
slack_router.register('show_tickets', SlackTicketsListViewSet,
                      basename='slack_show_tickets')
slack_router.register('display_dialog', SlackDialogViewSet,
                      basename='display_dialog')

urlpatterns = [
    path('',
         include(slack_router.urls),
         name='slack_information'),

    path('proceed_payload/',
         slack_payload,
         name='proceed_payload'),
]
