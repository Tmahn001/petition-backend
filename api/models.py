from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    signatures = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='signed_petitions', blank=True)

    def __str__(self):
        return self.title

class Signature(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    signer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    signed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.signer} signed {self.petition}"



