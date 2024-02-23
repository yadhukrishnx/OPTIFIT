# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from squats.consumers import WorkoutConsumer
from django.urls import path


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # Add routing for the WorkoutConsumer
            path('ws/squats/', WorkoutConsumer.as_asgi()),
        )
    ),
})