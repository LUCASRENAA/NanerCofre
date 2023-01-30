from rest_framework import serializers

from .models import BlocoNotasCriptografada,ChaveMestra,CredencialSites


class BlocoNotasCriptografadaSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BlocoNotasCriptografada
        fields = '__all__'


class CredencialSitesSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CredencialSites
        fields = '__all__'


class BlocoNotasCriptografadaSerializerID(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    titulo = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = BlocoNotasCriptografada
        fields = ['id']

class ChaveMestraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChaveMestra
        fields = '__all__'