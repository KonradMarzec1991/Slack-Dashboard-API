from django.urls import path
from .views import testview, display_dialog, proceed_payload

urlpatterns = [
    path('test/', testview, name='test'),
    path('display_dialog/', display_dialog, name='display_dialog'),
    path('proceed_payload/', proceed_payload, name='proceed_payload'),
]
