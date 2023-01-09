from rest_framework import serializers

from .models import BlocoNotasCriptografada,ChaveMestra


class BlocoNotasCriptografadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlocoNotasCriptografada
        fields = '__all__'

class BlocoNotasCriptografadaSerializerID(serializers.ModelSerializer):
    class Meta:
        model = BlocoNotasCriptografada
        fields = ['id']

class ChaveMestraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChaveMestra
        fields = '__all__'