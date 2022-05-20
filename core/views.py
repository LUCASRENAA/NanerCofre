import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import hashlib
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import models
from datetime import  datetime, timezone, timedelta


from core.models import Hash_Senha_Cofre,Arquivo
import time
from cryptography.fernet import Fernet
from cryptography import fernet
# Create your views here.



# Create your views here
from core.models import Senha_Criptografada


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
            return redirect('/')
        else:
            messages.error(request,"Usuário ou senha invalido")


    return  redirect('/')

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
            User.objects.get(usuario = usuario)
            User.objects.get(email = email)


            return HttpResponse('<h1> Usuario já cadastrado </h1>')

        print("hey")
        return redirect('/')
    return HttpResponse('<h1> faça um post </h1>')



@login_required(login_url='/login/')
def inicio(request):
    from cryptography.fernet import Fernet

    key = Fernet.generate_key()


    try:
        Hash_Senha_Cofre.objects.get(usuario = request.user)

        mensagem = "Digite sua senha"
    except:
        mensagem = "Crie sua senha"


    dados = {"key": key,"mensagem":mensagem}

    return render(request,'inicio.html',dados)

def senha_fernet(senha):
    import base64
    import os
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    password = bytes(senha,encoding='utf8')
    print(len(password))
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key



def hash_chave(key):
    import hashlib
    hash_Chave = hashlib.sha256()
    chave_que_vai = str(key).encode(encoding='utf8')

    hash_Chave.update(chave_que_vai)

    hash_texto_chave= hash_Chave.hexdigest()
    return hash_texto_chave

@login_required(login_url='/login/')
def inicio_submit(request):
    senha = request.POST.get('senha')

    #formato do fernet de senha
    key = str(senha)

    if len(key) < 44:
        key = key + "a" * (43 - len(key)) + "="

    key = key[0:44]

    #hash da senha

    try:
        cofre = Hash_Senha_Cofre.objects.get(
                                        usuario= request.user)
        hash_texto_chave = hash_chave(key)
        if (cofre.hash == hash_texto_chave):
            return render(request, 'cofre.html',{'senha':key,'cofre':Arquivo.objects.filter(hash__usuario=request.user),
                                                 'senhas_cofre': Senha_Criptografada.objects.filter(usuario=request.user)})



        return HttpResponse("senha errada")

    except:
        hash_texto_chave = hash_chave(key)
        Hash_Senha_Cofre.objects.create(hash=hash_texto_chave,
                                        usuario=request.user)
    dados = {"key":senha}
    print(key)
    return render(request,'exibir_senha.html',dados)


def decripitar(key,local="safasfsa.zip"):
        # using the key
        from cryptography.fernet import Fernet

        fernet = Fernet(key)

        # opening the encrypted file
        with open(local, 'rb') as enc_file:
            encrypted = enc_file.read()
            print(encrypted)
            print("aqui")

        # decrypting the file
        decrypted = fernet.decrypt(encrypted)

        return decrypted



def criptografar(key,file,dataAgora):
        from cryptography.fernet import Fernet

        # opening the key

        # using the generated key
        print(key)
        fernet = Fernet(key)

        # opening the original file to encrypt

        original = file.read()

        # encrypting the file
        encrypted = fernet.encrypt(original)

        # opening the file in write mode and
        # writing the encrypted data
        with open("salvar_Arquivos/'"+str(file)+str(dataAgora)+"'", 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

def criptografar_texto(key,texto):
    f = Fernet(key)
    token = f.encrypt(bytes(texto,encoding='utf-8'))

    return token


def descriptografar_texto(request):
    from urllib.parse import unquote
    key = request.POST.get('key')
    texto = request.POST.get('texto')

    key = unquote(key)
    texto = unquote(texto)


    key = str(key.replace("b'", "").replace("'", "")).encode(encoding='utf-8')
    print(key)
    f = Fernet(key)

    texto_vai = str(texto.replace("b'", "").replace("'", "")).encode(encoding='utf-8')
    valor = f.decrypt(texto_vai)
    return HttpResponse(str(valor.decode("ascii")))
def dataAtual():
    data_e_hora_atuais = datetime.now()
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    print(data_e_hora_sao_paulo)
    return str(data_e_hora_sao_paulo)


@login_required(login_url='/login/')
def subir_arquivo(request):






    file = request.FILES['file']
    senha = request.POST.get('senha')

    key = bytes(senha, encoding='ascii')



    senha = str(request.POST.get('senha')).encode('ascii')




    import hashlib


    dataAgora = dataAtual().replace(" ", "")
    criptografar(str(request.POST.get('senha').replace("b'","").replace("'","")).encode(encoding='utf-8'),file,dataAgora)
    #decripitar(key)

    senha = request.POST.get('senha')

    # formato do fernet de senha
    key = str(senha)

    if len(key) < 44:
        key = key + "a" * (43 - len(key)) + "="

    key = key[0:44]


    Arquivo.objects.create(hash=Hash_Senha_Cofre.objects.get(hash=hash_chave(str(senha)),usuario=request.user) ,local="salvar_Arquivos/"+str(file),dataAgora=dataAgora)

    dados = {"senha":key}
    return redirect('/')

@login_required(login_url='/login/')
def criptografar_texto_submit(request):
    senha = str(request.POST.get('senha').replace("b'","").replace("'","")).encode(encoding='utf-8')
    texto = request.POST.get('texto')
    titulo = request.POST.get('titulo')
    nome = request.POST.get('nome')
    senha_texto = request.POST.get('senha_texto')
    uri = request.POST.get('uri')

    #texto_criptografado  = criptografar_texto(senha,texto)
    titulo_criptografado  = criptografar_texto(senha,titulo)
    nome_criptografado  = criptografar_texto(senha,nome)
    senha_texto_criptografado  = criptografar_texto(senha,senha_texto)
    uri_criptografado  = criptografar_texto(senha,uri)

    Senha_Criptografada.objects.create(titulo=titulo_criptografado,
                                       nome=nome_criptografado,
                                       senha=senha_texto_criptografado,
                                       uri=uri_criptografado,
                                       usuario=request.user)
    dados = {'key':senha}
    return render(request,'exibir_senha.html',dados)


@login_required(login_url='/login/')
def descer_arquivo_path(request,id):
        arquivo = Arquivo.objects.get(id=id)
        nome = str(arquivo.local).replace("salvar_Arquivos/" , "")

        key = str(request.POST.get('senha').replace("b'","").replace("'","")).encode(encoding='utf-8')
        hash_Chave = hashlib.sha256()
        hash_Chave.update(key)

        hash_texto_chave = hash_Chave.hexdigest()

        print(key)
        print(arquivo.hash)
        print(hash_texto_chave)

        print(len(key))

        if str(arquivo.hash.hash) == str(hash_texto_chave):

            valor = decripitar(bytes(key),"salvar_Arquivos/'"+arquivo.local.replace("salvar_Arquivos/","")+arquivo.dataAgora+"'")
            teste = ""
            for a in valor:
                print(chr(a))
                teste = teste + chr(a)

            response = HttpResponse(valor, content_type='application/txt')
            response['Content-Disposition'] = 'attachment; filename="' + nome + '"'
            return response




