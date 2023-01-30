from django.contrib import admin

# Register your models here.

from api.models import BlocoNotasCriptografada,CredencialSites

admin.site.register(BlocoNotasCriptografada)
admin.site.register(CredencialSites)