from rest_framework.routers import SimpleRouter

from documents import views

app_name = 'document'
router = SimpleRouter()

router.register('documents', views.DocumentViewSet, 'documents')

urlpatterns = router.urls
