from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Petition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    signatures = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='signed_petitions', blank=True)
    involved_parties = models.ManyToManyField(
        'InvolvedParty',
        related_name='entities',
    )
    required_signatures_range = models.PositiveIntegerField(default=0)
    image= models.ImageField(upload_to='media/images/',null=True, blank=True)
    

    def __str__(self):
        return self.title

class InvolvedParty(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    office_address = models.TextField()


class Signature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    signer_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    signed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.signer_name} signed {self.petition}"




