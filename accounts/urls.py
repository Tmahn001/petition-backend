from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import EmailTokenObtainPairView, RegisterView

router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')
urlpatterns = [
    path('', include(router.urls)),
    path('token/obtain/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
