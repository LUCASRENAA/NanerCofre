from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

import os
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Protocol.KDF import PBKDF2
from django.contrib.auth.hashers import make_password,check_password

from api.models import BlocoNotasCriptografada, ChaveMestra


def descriptografar(request,id):
    key = request.POST.get('key')
    key = bytes(key, 'utf-8')

    try:
        chave = ChaveMestra.objects.get(user=request.user)
        hashed_pass = make_password(key)
        comparar = chave.texto

        print(hashed_pass)
        print(comparar)

        validador = check_password(key,comparar)





    except:
        exit()

    if validador:
        bloco = BlocoNotasCriptografada.objects.get(id=id,user=request.user)

        data = bloco.texto
        e_cipher = bloco.e_cipher

        d_data = decriptar(key, data, e_cipher)
        d_data = str(d_data)
        print(d_data)
        d_data = d_data[:-1]
        print(d_data)

        d_data = d_data[1:]
        d_data = d_data[1:]
        print(d_data)

        dados = {"titulo":bloco.titulo,"descricao":str(d_data),'id':bloco.id}
        return render(request,'frontend/index.html',dados)



def criptografar(request):





    if request.POST:
        title = request.POST.get('title')
        key = request.POST.get('key')
        description = request.POST.get('description')
        key = bytes(key, 'utf-8')
        id = request.POST.get('id')
        print(id)

        print(request.POST)
        deletar = request.POST.get('deletar')
        print(id)
        print("id em cima")
        hashed_pass = make_password(key)


        try:
            chave = ChaveMestra.objects.get(user=request.user)
            comparar = chave.texto
            validador = check_password(key, comparar)



        except:
                ChaveMestra.objects.create(user=request.user,texto=hashed_pass)
                validador = True
        if validador:
            description = bytes(description, 'utf-8')

            e_data, e_cipher = encriptar(key, description)
            try:
                bloco_editar = BlocoNotasCriptografada.objects.get(id=int(id), user=request.user)
                bloco_editar.titulo = title
                bloco_editar.texto = e_data
                bloco_editar.e_cipher = e_cipher.nonce
                bloco_editar.save()
                print("aqui")
            except:
                BlocoNotasCriptografada.objects.create(user=request.user, titulo=title, texto=e_data,
                                                       e_cipher=e_cipher.nonce)


        return redirect("/front/home")



def secreta(request):
    if request.user.is_superuser:
        return  HttpResponse("arquivo secreto")
    else:
        return HttpResponse("saia daqui que você não é administrador")

def cofre(request):
    return render(request, 'frontend/cofre.html')


def todos(request):

    if request.user.is_authenticated:

        dados = {"anotacoes": BlocoNotasCriptografada.objects.filter(user=request.user)}
        return render(request,'frontend/home.html',dados)
    else:
        return redirect('/login')


def teste(request):
    dados = {"anotacoes": BlocoNotasCriptografada.objects.filter(user=request.user)}
    return render(request,'frontend/teste.html',dados)

def geradorDeSenha(request):
    return render(request,'frontend/gerador_de_senha.html')

def home(request):
    #key = b'Sixteen byte key'
    #dados = "teste"
    #dados = bytes(dados, 'utf-8')
    #e_data, e_cipher = encriptar(key,dados)
    #dados = {"e_data": e_data,"e_cipher":e_cipher}
    dados = {}
    #print(dados)
    return render(request,'frontend/index.html',dados)


def encriptar(key,data):
    e_cipher = AES.new(key, AES.MODE_EAX)
    e_data = e_cipher.encrypt(data)
    return e_data,e_cipher
def decriptar(key,data,e_cipher):
    print(key)

    print(data)
    print(e_cipher)
    d_cipher = AES.new(key, AES.MODE_EAX, e_cipher)
    d_data = d_cipher.decrypt(data)
    return d_data



def login_user(request):
    return render(request,'login.html')


def registro(request):
    return render(request,'registro.html')


def logout_user(request):
    logout(request)
    return redirect('/')
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username,password=password)
        if usuario is not None:
            login(request,usuario)
            return redirect('/front/home')
        else:
            messages.error(request,"Usuário ou senha invalido")


    return  redirect('/login')

def submit_registro(request):
    print(request.POST)
    if request.POST:
        senha = request.POST.get('password')
        usuario = request.POST.get ( 'username' )
        email =   request.POST.get ( 'email' )
        try:
            print("e aqui?")


            user = User.objects.create_user ( str(usuario), str(email) ,  str(senha) )




        except:


            return HttpResponse('<h1> Usuario já cadastrado </h1>')

        print("hey")
        return redirect('/front/cofre')
    return HttpResponse('<h1> faça um post </h1>')