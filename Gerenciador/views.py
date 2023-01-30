import datetime
from datetime import timedelta

import matplotlib
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

# Create your views here.
#from Usuario.models import Senha_Criptografada
from api.models import CredencialSites


def check_admin(user):
   return user.is_superuser


def pegarData():
    current_time = datetime.datetime.now()
    ano = current_time.year
    mes = current_time.month
    dia = current_time.day
    data = current_time
    return ano,mes,dia,data

@user_passes_test(check_admin)
def inicio(request):
    import datetime

    ano,mes,dia,data = pegarData()
    dados = {"ano":ano,"mes":mes,"dia":dia,"data":data}
    return render(request,'Gerenciador/escolher.html',dados)

@user_passes_test(check_admin)
def contasCriadas(request,ano,mes,dia,opcao):
    #usuarios = User.objects.get(username= "TESAUIFHASUFHASIU1safas1f65a@!@").date_joined -timedelta(hours=3)
    usuarios_filtro = pegarUsuariosDataCriacao(ano,mes,dia,opcao)


    titulo = "Pessoas"
    cor_azul = "Pessoas Totais"
    cor_vermelha = "Pessoas que criaram a conta"
    texto_complementar= "Pessoas que criaram suas contas no"
    usuarios = User.objects.all()
    criarGrafico()
    mes_texto = Mes_String(int(mes))
    if opcao == "1":
        texto_opcao = "anual"
        texto_embaixo = "Ano de " + ano
    if opcao == "2":
        texto_opcao = "mensal"
        texto_embaixo = "Ano de " + ano + " Mês de " + mes_texto
    if opcao == "3":
        texto_opcao = "diario"
        texto_embaixo = "Ano de " + ano + " Mês de " + mes_texto + " Dia "+ (dia)

    senhas_criptografadas = CredencialSites.objects.all()
    usuarios_que_vao  = []
    for usuario_filtro in usuarios_filtro:
        print(usuario_filtro)
        senhas = CredencialSites.objects.filter(user=usuario_filtro)
        print(senhas)
        usuarios_que_vao.append(Usuario_Quantidade_senhas(usuario_filtro,senhas))

    ano2, mes, dia, data = pegarData()

    dados = {"ano":ano,"titulo":titulo,"azul":cor_azul,"vermelho":cor_vermelha,"texto_complementar":texto_complementar,
        "usuarios_vetor":usuarios_que_vao,"senhas_criptografadas":senhas_criptografadas,
             "ano2": ano2, "mes": mes, "dia": dia, "data": data,"texto_embaixo":texto_embaixo,"usuarios":usuarios,'usuario_filtro':usuarios_filtro,'pagina':"Usuario",'opcao':opcao,"texto_opcao":texto_opcao}
    return render(request,'Gerenciador/gerenciador.html',dados)

@user_passes_test(check_admin)
def usuariosSemSenhas(request):
    ano_pegar, mes_pegar, dia_pegar, data_pegar = pegarData()

    #usuarios = User.objects.get(username= "TESAUIFHASUFHASIU1safas1f65a@!@").date_joined -timedelta(hours=3)
    usuarios = User.objects.all()
    usuarios_filtro = []
    texto_opcao = " (Usuários sem senhas)"
    class UsuaioSemSenha:
        def __init__(self, senhas, usuario):
            self.senhas = senhas
            self.usuario = usuario



    for usuario in usuarios:
        if len(CredencialSites.objects.filter(user=usuario)) == 0:

            usuarios_filtro.append(UsuaioSemSenha(CredencialSites.objects.filter(user=usuario),usuario))


    titulo = "Pessoas"
    cor_azul = "Pessoas com senhas"
    cor_vermelha = "Pessoas que não colocaram senhas"
    texto_complementar= "Pessoas que não colocaram senhas"


    dados = {"titulo":titulo,"azul":cor_azul,"vermelho":cor_vermelha,"texto_complementar":texto_complementar,
      "texto_opcao":texto_opcao,"usuarios_vetor":usuarios_filtro,"usuarios":usuarios,'usuario_filtro':usuarios_filtro,'pagina':"Usuario",
             "ano":ano_pegar,"mes":mes_pegar,"dia":dia_pegar,"ano2":ano_pegar}
    return render(request,'Gerenciador/gerenciador.html',dados)

@user_passes_test(check_admin)
def usuarioSenhas(request,usuario,ano):
    ano_pegar, mes_pegar, dia_pegar, data_pegar = pegarData()


    #usuarios = User.objects.get(username= "TESAUIFHASUFHASIU1safas1f65a@!@").date_joined -timedelta(hours=3)
    usuario= User.objects.get(username=usuario)
    senhas = CredencialSites.objects.filter(usuario=usuario)
    titulo = "Modificações no chaveiro por mês do usuário " + str(usuario)
    sub_titulo = "Ano de " + ano

    meses = []

    ano_real = datetime.datetime.now().year

    lista_ano = []
    for a in range(0, 10):
        lista_ano.append(int(ano_real) - a)




    class Usuario_Mes:
        def __init__(self, senhas, mes):
            self.senhas = senhas
            self.mes = mes
    for mes in range(1,13):
        senhas = CredencialSites.objects.filter(usuario=usuario,
                                                   modified_date__year=ano,
                                                   modified_date__month=mes,
                                                   )


        meses.append(Usuario_Mes(senhas,Mes_String(mes)))





    dados = {"mes":mes_pegar,"dia":dia_pegar,"senhas":meses,'ano':ano,'titulo':titulo,'subtitulo':sub_titulo,'usuario': request.user,"anos":lista_ano}
    return render(request,'Gerenciador/usuario_criacao.html',dados)


@user_passes_test(check_admin)
def usuarioGeral(request,ano):
    ano_pegar, mes_pegar, dia_pegar, data_pegar = pegarData()

    #usuarios = User.objects.get(username= "TESAUIFHASUFHASIU1safas1f65a@!@").date_joined -timedelta(hours=3)
    usuarios= User.objects.all()
    senhas = CredencialSites.objects.all()
    titulo = "Quantidade de senhas no chaveiro por mês de todos os usuarios"

    meses = []
    ano_real =     datetime.datetime.now().year

    lista_ano = []
    for a in range(0,10):
        lista_ano.append(int(ano_real)-a)
    class Usuario_Mes:
        def __init__(self, senhas, mes):
            self.senhas = senhas
            self.mes = mes
    for mes in range(1,13):
        senhas = CredencialSites.objects.filter(
                                                   created_date__year=ano,
                                                   created_date__month=mes,
                                                   )


        meses.append(Usuario_Mes(senhas,Mes_String(mes)))



    dados = {"titulo":titulo,"senhas":meses,'ano':ano,'usuario': request.user,"anos":lista_ano,"mes":mes_pegar,"dia":dia_pegar}
    return render(request,'Gerenciador/usuarios.html',dados)



@user_passes_test(check_admin)
def usuarioSenhasCriacao(request,usuario,ano):
    ano_pegar, mes_pegar, dia_pegar, data_pegar = pegarData()


    #usuarios = User.objects.get(username= "TESAUIFHASUFHASIU1safas1f65a@!@").date_joined -timedelta(hours=3)
    usuario= User.objects.get(username=usuario)
    senhas = CredencialSites.objects.filter(user=usuario)
    titulo = "Modificações no chaveiro por mês do usuário " + str(usuario)
    sub_titulo = "Ano de " + ano

    meses = []

    ano_real = datetime.datetime.now().year

    lista_ano = []
    for a in range(0, 10):
        lista_ano.append(int(ano_real) - a)




    class Usuario_Mes:
        def __init__(self, senhas, mes):
            self.senhas = senhas
            self.mes = mes
    for mes in range(1,13):
        senhas = CredencialSites.objects.filter(user=usuario,
                                                   created_date__year=ano,
                                                   created_date__month=mes,
                                                   )


        meses.append(Usuario_Mes(senhas,Mes_String(mes)))





    dados = {"mes":mes_pegar,"dia":dia_pegar,"senhas":meses,'ano':ano,'titulo':titulo,'subtitulo':sub_titulo,'usuario': request.user,"anos":lista_ano}
    return render(request,'Gerenciador/usuario_criacao.html',dados)


@user_passes_test(check_admin)
def usuarioGeralCriacao(request,ano):
    ano_pegar, mes_pegar, dia_pegar, data_pegar = pegarData()

    #usuarios = User.objects.get(username= "TESAUIFHASUFHASIU1safas1f65a@!@").date_joined -timedelta(hours=3)
    usuarios= User.objects.all()
    senhas = CredencialSites.objects.all()
    titulo = "Quantidade de senhas no chaveiro por mês de todos os usuarios"

    meses = []
    ano_real =     datetime.datetime.now().year

    lista_ano = []
    for a in range(0,10):
        lista_ano.append(int(ano_real)-a)
    class Usuario_Mes:
        def __init__(self, senhas, mes):
            self.senhas = senhas
            self.mes = mes
    for mes in range(1,13):
        senhas = CredencialSites.objects.filter(
                                                   modified_date__year=ano,
                                                   modified_date__month=mes,
                                                   )


        meses.append(Usuario_Mes(senhas,Mes_String(mes)))



    dados = {"titulo":titulo,"senhas":meses,'ano':ano,'usuario': request.user,"anos":lista_ano,"mes":mes_pegar,"dia":dia_pegar}
    return render(request,'Gerenciador/usuarios.html',dados)

class Usuario_Quantidade_senhas:
        def __init__(self, usuario, quantidade):
            self.usuario = usuario
            self.quantidade = quantidade
def pegarUsuariosDataCriacao(ano,mes,dia,opcao):
    if opcao == "3":
        usuarios = User.objects.filter(date_joined__year=ano,
                                       date_joined__month=mes,
                                       date_joined__day=dia)



    if opcao == "2":
        usuarios = User.objects.filter(date_joined__year=ano,
                                       date_joined__month=mes)

    if opcao == "1":
        usuarios = User.objects.filter(date_joined__year=ano)

    return usuarios



def criarGrafico():
    import matplotlib.pyplot as plt
    import numpy as np
    matplotlib.use('Agg')

    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    men_means = [20, 34, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, men_means, width, label='Men')
    rects2 = ax.bar(x + width / 2, women_means, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()


def Mes_String(shortMonth):
        return {
           1: 'Janeiro',
           2: 'Fevereiro',
            3: 'Março',
            4: 'Abril' ,
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro"
        }[shortMonth]

