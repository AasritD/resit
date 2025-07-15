from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('user_management.urls')),
    path('billing/', include('billing_app.urls')),
    path('inference/', include('inference_app.urls')),
    path('uploads/', include('uploads.urls')),
]
