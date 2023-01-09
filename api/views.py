from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from api.models import BlocoNotasCriptografada, ChaveMestra
from api.serializeres import BlocoNotasCriptografadaSerializer, ChaveMestraSerializer, \
    BlocoNotasCriptografadaSerializerID
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView

from frontend.views import decriptar


class BlocoNotasCriptografadaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BlocoNotasCriptografadaSerializer
    def list(self,request):
        import json

        key = self.request.query_params['key']
        print(self.request.data)
        key = bytes(key, 'utf-8')
        dados = []
        for bloco in BlocoNotasCriptografada.objects.filter( user=request.user):
            data = bloco.texto
            e_cipher = bloco.e_cipher
            try:
                d_data = decriptar(key, data, e_cipher)
            except:
                d_data = "b''"
            d_data = str(d_data)
            print(d_data)
            d_data = d_data[:-1]
            print(d_data)

            d_data = d_data[1:]
            d_data = d_data[1:]

            dados.append({'titulo':str(bloco.titulo),'descricao':str(d_data),'id':bloco.id})
            print(d_data)
        print(dados)
        return HttpResponse(json.dumps(dados), content_type="application/json")

    queryset = BlocoNotasCriptografada.objects.all()



    http_method_names = ['get', 'post', 'put', 'path','delete']



class ChaveMestraViewSet(viewsets.ModelViewSet):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    #permission_classes = [permissions.AllowAny]
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAdmin]

    def list(self,request):
        dados = []
        import json
        bloco = ChaveMestra.objects.get(user=request.user)

        dados.append({'texto':str(bloco.texto),'id':bloco.id})
        print(dados)
        return HttpResponse(json.dumps(dados), content_type="application/json")
    queryset = ChaveMestra.objects.all()
    serializer_class = ChaveMestraSerializer
    http_method_names = ['get', 'post', 'put', 'path','delete']