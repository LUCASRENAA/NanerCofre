from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from api.models import BlocoNotasCriptografada, ChaveMestra,CredencialSites
from api.serializeres import BlocoNotasCriptografadaSerializer, ChaveMestraSerializer, \
    BlocoNotasCriptografadaSerializerID,CredencialSitesSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView

from frontend.views import decriptar
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Protocol.KDF import PBKDF2
from django.contrib.auth.hashers import make_password,check_password

from rest_framework import filters

class URIFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        uri = request.query_params.get('uri', None)
        if uri is not None:
            queryset = queryset.filter(uri=uri)
        return queryset

def encriptar(key,data):
    e_cipher = AES.new(key, AES.MODE_EAX)
    e_data = e_cipher.encrypt(data)
    return e_data,e_cipher
def decriptar(key,data,e_cipher):
    #print(key)

    #print(data)
    #print(e_cipher)
    d_cipher = AES.new(key, AES.MODE_EAX, e_cipher)
    d_data = d_cipher.decrypt(data)
    return d_data


class BlocoNotasCriptografadaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BlocoNotasCriptografadaSerializer
    def list(self,request):
        import json

        key = self.request.query_params['key']
        #print(self.request.data)
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
            #print(d_data)
            d_data = d_data[:-1]
            #print(d_data)

            d_data = d_data[1:]
            d_data = d_data[1:]

            dados.append({'titulo':str(bloco.titulo),'descricao':str(d_data),'id':bloco.id})
            #print(d_data)
        #print(dados)
        return HttpResponse(json.dumps(dados), content_type="application/json")

    queryset = BlocoNotasCriptografada.objects.all()

    def destroy(self, request, *args, **kwargs):
        from rest_framework import status

        instance = self.get_object()
        if instance.user != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user:
            raise PermissionDenied()
        print("aqui")
        data = self.request.data.copy()
        key = data.get('key')

        titulo = data.get('titulo')
        try:
            texto = data.get('texto')
            key = bytes(str(key), 'utf-8')
            texto = bytes(texto, 'utf-8')
            e_data, e_cipher = encriptar(key, texto)

            # data.update({'texto': "teste","user":self.request.user.id})
            print(e_data)
            print(e_cipher)
            print("aqui")
            if titulo == "+":
                serializer.save(texto=e_data, e_cipher=e_cipher.nonce, user=self.request.user)

            else:
                serializer.save(titulo=titulo, texto=e_data, e_cipher=e_cipher.nonce, user=self.request.user)
        except:
            serializer.save(titulo=titulo)




    def perform_create(self, serializer):
        data = self.request.data.copy()

        key = data.get('key')

        texto =  data.get('texto')
        key = bytes(str(key), 'utf-8')
        texto = bytes(texto, 'utf-8')

        e_data, e_cipher =     encriptar(key,texto)

        #data.update({'texto': "teste","user":self.request.user.id})
        serializer.save(texto=e_data,e_cipher=e_cipher.nonce,user=self.request.user)
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

def limparbyte(d_data):
    d_data = d_data[:-1]
    d_data = d_data[1:]
    d_data = d_data[1:]
    return d_data

class CredencialSitesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CredencialSitesSerializer
    http_method_names = ['get', 'post', 'put', 'path','delete']

    def list(self,request):
        import json

        key = self.request.query_params['key']
        print(self.request.data)
        key = bytes(key, 'utf-8')
        dados = []

        try:
            uri = self.request.query_params['uri']

            blocos = CredencialSites.objects.filter(user=request.user, uri=uri)
        except:
            blocos = CredencialSites.objects.filter(user=request.user)
        for bloco in blocos:
            data = bloco.nome
            e_cipher = bloco.e_cipher_nome
            uri = bloco.uri

            senha = bloco.senha
            e_cipher_senha = bloco.e_cipher_senha

            notas = bloco.notas
            e_cipher_notas = bloco.e_cipher_notas
            try:
                d_data = str(decriptar(key, data, e_cipher))
                d_data_senha = str(decriptar(key, senha, e_cipher_senha))
                d_data_nota = str(decriptar(key, notas, e_cipher_notas))

            except:
                d_data = "b''"
            d_data = limparbyte(d_data)
            d_data_senha = limparbyte(d_data_senha)
            d_data_nota = limparbyte(d_data_nota)

            dados.append({'titulo':str(bloco.titulo),'nome':str(d_data),'id':bloco.id,'uri':uri,'senha':d_data_senha,
                          'nota':d_data_nota})
            #print(d_data)
        #print(dados)
        return HttpResponse(json.dumps(dados), content_type="application/json")

    queryset = CredencialSites.objects.all()

    def destroy(self, request, *args, **kwargs):
        from rest_framework import status
        print("teste")
        instance = self.get_object()
        if instance.user != self.request.user:
            print("alo")
            return Response(status=status.HTTP_403_FORBIDDEN)
        print("estou aqui")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user:
            raise PermissionDenied()
        #print("aqui")
        data = self.request.data.copy()
        key = data.get('key')

        titulo = data.get('titulo')
        if 1 == 1:
            key = bytes(str(key), 'utf-8')
            texto = data.get('senha')

            texto = bytes(texto, 'utf-8')
            print(texto)
            e_data, e_cipher = encriptar(key, texto)

            notas = data.get('notas')

            notas = bytes(notas, 'utf-8')

            e_data_notas, e_cipher_notas = encriptar(key, notas)

            nome = data.get('nome')

            nome = bytes(nome, 'utf-8')

            e_data_nome, e_cipher_nome = encriptar(key, nome)

            serializer.save(titulo=titulo, senha=e_data, e_cipher_senha=e_cipher.nonce,
                            nome=e_data_nome,e_cipher_nome=e_cipher_nome.nonce,
                            notas=e_data_notas,e_cipher_notas=e_cipher_notas.nonce,

                            user=self.request.user)




    def perform_create(self, serializer):
        data = self.request.data.copy()

        key = data.get('key')

        texto =  data.get('nome')
        senha =  data.get('senha')
        notas =  data.get('notas')


        key = bytes(str(key), 'utf-8')
        texto = bytes(texto, 'utf-8')
        senha = bytes(senha, 'utf-8')
        notas = bytes(notas, 'utf-8')

        e_data, e_cipher =     encriptar(key,texto)
        e_data_senha, e_cipher_senha =     encriptar(key,senha)
        e_data_notas, e_cipher_notas =     encriptar(key,notas)

        #data.update({'texto': "teste","user":self.request.user.id})
        serializer.save(nome=e_data,e_cipher_nome=e_cipher.nonce,user=self.request.user,
                        senha=e_data_senha,e_cipher_senha=e_cipher_senha.nonce,
                        notas=e_data_notas,e_cipher_notas=e_cipher_notas.nonce)

