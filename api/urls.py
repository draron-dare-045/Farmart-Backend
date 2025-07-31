from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnimalViewSet,
    OrderViewSet,
    MakePaymentView,
    MpesaCallbackView,
    UserProfileView,
    RegisterUserView,
    FarmerProfessionalDashboardView, 
)


router.register(r'animals', AnimalViewSet, basename='animal')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    path('dashboard/pro-stats/', FarmerProfessionalDashboardView.as_view(), name='farmer-pro-stats'),
    path('make-payment/', MakePaymentView.as_view(), name='make-payment'),
    path('mpesa-callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
]