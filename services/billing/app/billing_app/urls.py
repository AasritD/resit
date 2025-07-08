from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UsageViewSet, InvoiceViewSet

router=DefaultRouter()
router.register('usage', UsageViewSet, basename='usage')
router.register('invoice', InvoiceViewSet, basename='invoice')

urlpatterns=[ path('api/',include(router.urls)), ]
