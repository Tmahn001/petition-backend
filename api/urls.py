from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetitionViewSet, SignatureViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'petitions', PetitionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('petitions/<uuid:petition_id>/authenticated_sign/', SignatureViewSet.as_view({'post': 'perform_create_for_authenticated'}), name='authenticated-sign'),
    path('petitions/<uuid:petition_id>/sign_anonymously/', SignatureViewSet.as_view({'post': 'sign_anonymously'}), name='sign-anonymously'),
]




