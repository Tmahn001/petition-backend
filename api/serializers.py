from rest_framework import serializers
from .models import Petition, Signature, InvolvedParty
from drf_extra_fields.fields import Base64ImageField, Base64FileField

class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = ['id', 'petition', 'signer_name', 'student_email', 'signed_at']

    def validate_email(self, value):
        lower_value = value.lower()
        if ".edu" not in lower_value:
            raise serializers.ValidationError("This is not a valid student's email address")
        
        return value

class InvolvedPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvolvedParty
        fields = ['id', 'full_name', 'email', 'phone_number', 'office_address']

class PetitionSerializer(serializers.ModelSerializer):
    involved_parties = InvolvedPartySerializer(many=True, read_only=True)
    signatures = SignatureSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Petition
        fields = ['id', 'title', 'description', 'created_at', 'creator', 'signatures','involved_parties', 'required_signatures_range', 'image']
        read_only_fields = ['created_at', 'creator']

    



