from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/bot/status/$", consumers.BotStatusConsumer.as_asgi()),
    re_path(r'ws/positions/$', consumers.BotStatusConsumer.as_asgi()),
]
