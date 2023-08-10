from rest_framework import serializers
from .models import Petition, Signature

class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        exclude = ['signed_at']

class PetitionSerializer(serializers.ModelSerializer):
    signatures = SignatureSerializer(many=True, read_only=True)

    class Meta:
        model = Petition
        exclude = ['created_at']
