from django.urls import path

from .views import (
    display_dialog,
    proceed_payload,
    show_my_tickets,
    test_layout
)

urlpatterns = [
    path('display_dialog/', display_dialog, name='display_dialog'),
    path('proceed_payload/', proceed_payload, name='proceed_payload'),
    path('show_tickets/', show_my_tickets, name='show_tickets'),
    path('test_layout/', test_layout, name='test_layout'),
]