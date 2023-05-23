from django.conf import settings
from django.contrib import admin
from django.urls import path

from .debug import debug_toolbar_urlpatterns
from .static import static_urlpatterns

admin.site.site_header = settings.ADMIN_SITE_NAME

urlpatterns = debug_toolbar_urlpatterns + [
    path('', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static_urlpatterns
