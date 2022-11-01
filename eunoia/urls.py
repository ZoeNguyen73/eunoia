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
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from auth.auth import CustomObtainTokenPairView

from organizations.views import OrganizationViewSet, OrganizationViewByTypeSet
from users.views import UserViewSet, UserActivateView, UserActivateRequestView
from carts.views import CartViewSet

router = DefaultRouter()
router.register(r'api/v1/organizations', OrganizationViewSet, basename='organizations')
router.register(r'api/v1/users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/carts/', CartViewSet.as_view({'post': 'create', 'get': 'retrieve'}), name='cart_create_retrieve'),
    path('api/v1/listings/', include('listings.urls')),
    path('api/v1/listings/<id>/timeslots/', include('timeslots.urls')),
    path('api/v1/organizations/<slug>/addresses/', include('addresses.urls')),
    path('api/v1/organizations/<slug>/items/', include('items.urls')),
    path('api/v1/organizations/<slug>/', include('organizations.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/auth/token/', CustomObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/users/activate/<token>', UserActivateView.as_view({'patch': 'partial_update'}), name='activate'),
    path('api/v1/users/request-activate/', UserActivateRequestView.as_view({'patch': 'partial_update'}), name='activate_request'),
    path('api/v1/organizations/types/<type>/', OrganizationViewByTypeSet.as_view({'get': 'list'}), name='organization_type'),
    path('', include(router.urls)),
]
