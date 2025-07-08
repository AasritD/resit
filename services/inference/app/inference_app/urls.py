from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModelArtifactViewSet, InferenceViewSet, upload_ui

router = DefaultRouter()
router.register('artifacts', ModelArtifactViewSet, basename='artifact')
router.register('predict', InferenceViewSet, basename='inference')

urlpatterns = [
  path('api/', include(router.urls)),
  path('upload/', upload_ui, name='upload_ui'),
]
