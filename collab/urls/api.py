from django.conf import settings
from django.urls import include, path

from .debug import debug_toolbar_urlpatterns
from .static import static_urlpatterns

__all__ = ['urlpatterns']

urlpatterns = [
    path('auth/', include(('users.urls', 'users'), namespace='auth')),
] + debug_toolbar_urlpatterns

if settings.DEBUG:
    urlpatterns += static_urlpatterns
