from rest_framework import viewsets, status
from .models import Petition, Signature
from .serializers import PetitionSerializer, SignatureSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from accounts.models import CustomUser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

class PetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(creator=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AllowUnauthenticated(BasePermission):
    """
    Allow unauthenticated access to specific actions.
    """

    def has_permission(self, request, view):
        if view.action == 'sign_anonymously':
            return True
        return request.user and request.user.is_authenticated

class SignatureViewSet(viewsets.ModelViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def sign(self, request, petition_id):
        petition = get_object_or_404(Petition, id=petition_id)
        
        if request.user.is_authenticated:
            serializer = SignatureSerializer(data={
                'petition': petition_id,
                'signer_name': request.user.first_name + ' ' + request.user.last_name,
                'student_email': request.user.email,
            })
        else:
            serializer = SignatureSerializer(data={
                'petition': petition_id,
                'signer_name': request.data.get('signer_name'),
                'student_email': request.data.get('student_email'),
            })

        if serializer.is_valid():
            serializer.save(petition=petition)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create_for_unauthenticated(self, request, petition_id):
        petition = get_object_or_404(Petition, id=petition_id)
        serializer = SignatureSerializer(data={
            'petition': petition_id,
            'signer_name': request.data.get('signer_name'),
            'student_email': request.data.get('student_email'),
        })
        if serializer.is_valid():
            serializer.save(petition=petition)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


'''class UserDetailsView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        #user_id = kwargs.get('user_id')
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        petitions_created = Petition.objects.filter(creator=user)
        signed_petitions = Petition.objects.filter(signatures__student_email=request.user.email)

        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'petitions_created': PetitionSerializer(petitions_created, many=True).data,
            'total_petitions_created': petitions_created.count(),
            'signed_petitions': PetitionSerializer(signed_petitions, many=True).data,
            'total_signed_petitions': signed_petitions.count(),
        }

        return Response(user_data)'''

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        petitions_created = Petition.objects.filter(creator=user)
        signed_petitions = Petition.objects.filter(signature__student_email__isnull=False)

        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'petitions_created': [
                {
                    'petition': PetitionSerializer(petition).data,
                    'total_signatures': petition.signatures.count(),
                }
                for petition in petitions_created
            ],
            'total_petitions_created': petitions_created.count(),
            
        }

        return Response(user_data)
