from django.contrib import admin
from .models import Petition, InvolvedParty, Signature

# Define ModelAdmin classes for your models
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at', 'required_signatures_range')
    list_filter = ('created_at',)
    search_fields = ('title', 'creator__username')
    filter_horizontal = ('signatures', 'involved_parties')

class InvolvedPartyAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number')
    search_fields = ('full_name', 'email')

class SignatureAdmin(admin.ModelAdmin):
    list_display = ('signer_name', 'student_email', 'petition', 'signed_at')
    list_filter = ('signed_at',)
    search_fields = ('signer_name', 'student_email', 'petition__title')

# Register your models using the custom ModelAdmin classes
admin.site.register(Petition, PetitionAdmin)
admin.site.register(InvolvedParty, InvolvedPartyAdmin)
admin.site.register(Signature, SignatureAdmin)

