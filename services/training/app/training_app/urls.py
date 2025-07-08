from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingViewSet, ExperimentRunViewSet

router = DefaultRouter()
router.register(r'experiment-runs', ExperimentRunViewSet, basename='experimentrun')
router.register(r'training', TrainingViewSet, basename='training')

urlpatterns = [
    path('', include(router.urls)),
]
