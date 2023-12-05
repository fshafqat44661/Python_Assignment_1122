import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatsapp_api.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter(
        routing.websocket_urlpatterns
    ),
})
