from rest_framework import viewsets
from .models import Petition, Signature
from .serializers import PetitionSerializer, SignatureSerializer
from rest_framework.permissions import IsAuthenticated

class PetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class SignatureViewSet(viewsets.ModelViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        petition_id = self.request.data.get('petition')
        petition = get_object_or_404(Petition, pk=petition_id)
        serializer.save(signer=self.request.user, petition=petition)
