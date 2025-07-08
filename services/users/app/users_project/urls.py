from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
  path('admin/', admin.site.urls),
  path('api/auth/', TokenObtainPairView.as_view(), name='token_obtain'),
  path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('api/users/', include('users_app.urls')),
]
