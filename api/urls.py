from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnimalViewSet,
    OrderViewSet,
    UserProfileView,
    RegisterUserView,
)

router = DefaultRouter()
router.register(r'animals', AnimalViewSet, basename='animal')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
]