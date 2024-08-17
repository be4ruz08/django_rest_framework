"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.messages import api
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.authtoken import views
from django.conf import settings

from olcha.views.auth.views import RegisterAPIView
from root import custom_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenBlacklistView
from root.custom_obtain_views import LogoutApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('olcha-uz/', include('olcha.urls')),
    path('post/', include('post.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', custom_token.CustomAuthToken.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('logout-page/', LogoutApiView.as_view()),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

