from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_management.urls', namespace='user_management')),
    path('uploads/', include('uploads.urls', namespace='uploads')),
    path('inference/', include('inference_app.urls')),
    path('billing/', include('billing_app.urls')),
]
