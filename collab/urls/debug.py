from django.conf import settings
from django.urls import include, path

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    debug_toolbar_urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
else:
    debug_toolbar_urlpatterns = []
