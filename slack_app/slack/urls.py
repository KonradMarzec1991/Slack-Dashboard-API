from django.urls import path

from .views import (
    display_dialog,
    proceed_payload,
    show_my_tickets,
    display_information,
)

urlpatterns = [
    path('display_dialog/', display_dialog, name='display_dialog'),
    path('display_information/', display_information, name='display_information '),
    path('proceed_payload/', proceed_payload, name='proceed_payload'),
    path('show_tickets/', show_my_tickets, name='show_tickets'),
]
