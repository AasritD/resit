from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModelArtifactViewSet, InferenceViewSet, upload_ui, dashboard

router = DefaultRouter()
router.register(r'artifacts', ModelArtifactViewSet, basename='artifact')
router.register(r'infer',    InferenceViewSet,     basename='infer')

app_name = 'inference_app'

urlpatterns = [
    path('api/', include((router.urls, app_name), namespace='api')),
    path('upload/', upload_ui,   name='upload'),
    path('dashboard/', dashboard, name='dashboard'),
]
