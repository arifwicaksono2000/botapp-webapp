# asgi.py
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.conf import settings # Import settings
import botcore.routing # Assuming botcore.routing is correctly set up

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djbotapp.settings')

# Get the base HTTP ASGI application
http_application = get_asgi_application()

# If in DEBUG mode, wrap the HTTP application with StaticFilesHandler
# if settings.DEBUG:
#     from django.contrib.staticfiles.handlers import StaticFilesHandler
#     http_application = StaticFilesHandler(http_application)

application = ProtocolTypeRouter({
    "http": http_application,  # Use the (potentially wrapped) HTTP application
    "websocket": AuthMiddlewareStack(
        URLRouter(
            botcore.routing.websocket_urlpatterns
        )
    ),
})



