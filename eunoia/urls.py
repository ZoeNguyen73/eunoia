"""eunoia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from organizations.views import OrganizationViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'api/v1/organizations', OrganizationViewSet, basename='organizations')
router.register(r'api/v1/users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('organizations/', include('organizations.urls'))
    path('api/v1/users/<username>/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
