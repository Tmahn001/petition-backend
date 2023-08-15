from rest_framework import viewsets, status
from .models import Petition, Signature
from .serializers import PetitionSerializer, SignatureSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from accounts.models import CustomUser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

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

''''class SignatureViewSet(viewsets.ModelViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [AllowUnauthenticated | IsAuthenticated]

    def perform_create(self, serializer, petition_id):
        #petition_id = self.request.data.get('petition')
        petition = get_object_or_404(Petition, id=petition_id)
        serializer.save(signer=self.request.user, petition=petition)

    def perform_create_for_authenticated(self, serializer, petition_id):
        petition = get_object_or_404(Petition, id=petition_id)
        if self.request.user.is_authenticated:
            serializer.save(signer=self.request.user, petition=petition)
        else:
            return Response({"error": "Authentication required"}, status=401)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def sign_anonymously(self, request, petition_id):
        #petition_id = self.request.data.get('petition')
        print(petition_id)
        petition = get_object_or_404(Petition, id=petition_id)
        signer_name = request.data.get('signer_name')
        student_email = request.data.get('student_email')

        if CustomUser.objects.filter(email=student_email).exists():
            return Response({"error": "Email is already registered"}, status=400)
        
        serializer = SignatureSerializer(data={
            'petition': petition_id,
            'signer_name': signer_name,
            'student_email': student_email
        })
        
        if serializer.is_valid():
            serializer.save(petition=petition)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)'''
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