from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetitionViewSet, SignatureViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'petitions', PetitionViewSet)
router.register(r'signatures', SignatureViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]