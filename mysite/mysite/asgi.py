
import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
import chatapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
        'http':get_asgi_application(),
        'websocket':AuthMiddlewareStack(
            URLRouter(
                chatapp.routing.websocket_urlpatterns
            )
        )  
})
