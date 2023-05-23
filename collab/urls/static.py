from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

static_urlpatterns = staticfiles_urlpatterns() + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
