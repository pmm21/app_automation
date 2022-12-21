from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/selenium/cpu-info/", consumers.CPUInfoConsumer.as_asgi()),
]