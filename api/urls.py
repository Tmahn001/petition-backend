from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetitionViewSet, SignatureViewSet, UserDetailsView

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'petitions', PetitionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('me/', UserDetailsView.as_view(), name='me'),
    path('petitions/<uuid:petition_id>/sign/', SignatureViewSet.as_view({'post': 'sign'}), name='sign-petition'),
]





