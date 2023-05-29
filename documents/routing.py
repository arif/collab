from django.urls import re_path

from documents import consumers

websocket_urlpatterns = [
    re_path(r'^ws/doc/(?P<id>\d+)/edit/$', consumers.DocumentConsumer.as_asgi()),
]
