# LunerCofre
## O seu cofre de senhas e arquivos

O LunerCofre é uma aplicação desenvolvida em Python(Django)
Para armazenamento de arquivos e senhas seguras.

Utilizando a biblioteca do Fernet para criptografar seus arquivos possibilitando que só o usuário com a chave mestra, acesse o arquivo.

## Objetivos
A aplicação Naner Cofre tem como objetivo armazenar senhas e arquivos de forma segura.

## Artigo

Está no link do Drive: https://drive.google.com/file/d/1RdB18Ai9pLVCiRCdOqVmxRI8QB_I1epG/view?usp=sharing


# Requisitos
- [x] Criar senha
- [x] Criptografar Arquivos
- [x] Visualizar Arquivos
- [ ] Melhorar tela do cofre
- [ ] Melhorar tela antes de entrar do cofre
- [ ] Corrigir bug de senha mestra
- [ ] Gerar senhas
- [ ] Aplicar Filtros
- [ ] Painel Administrativo
- [x] Verificar quantos usuarios e quais foram criados num filtro de ano,mes,dia
- [x] Verificar as modificações no chaveiro de um usuário
- [x] Verificar as modificações no chaveiro de todos os usuários (mes)
- [ ] Verificar as modificações no chaveiro de todos os usuários (dia)
- [ ] Verificar as modificações no chaveiro de todos os usuários (ano)
- [ ] Verificar usuários sem senhas
- [ ] Verificar usuários que mais utilizam
- [ ] Criar extensão pro chrome

# Tela Login
![vuln2.jpg](imagens_readme/login.png)

# Tela Entrar No Cofre
![vuln2.jpg](imagens_readme/entrar_no_cofre.png)

# Tela do cofre (Ainda em modificação)
![vuln2.jpg](imagens_readme/cofre.jpeg)


## Demonstração
A demonstração da ferramente será realizada através de um video ensinando a configurar o ambiente e o demonstrará O funcionamento da ferramenta será mostrado através da perspectiva do usuário e a outra do administrador e seguirá os seguintes passos (a) configurando o servidor, (b) armazenando senhas no servidor e (c) observando os gráficos e indicadores do sistema sobre a utilização do mesmo pelos usuários.


```
(a): https://drive.google.com/file/d/1gA3JS2y3r3SLsj3RdA1ufpa3Ry1QoaV7/view?usp=sharing
(b): https://drive.google.com/file/d/1d74OCjOrUfFtd6pP7dzJPf2AqNrDBZg6/view?usp=sharing
(c): https://drive.google.com/file/d/1FlpCdZx7wqoX7sLQp6GCAxm8WNbfLA70/view?usp=sharing
```

## Como usar?

### Primeiro acesso

```
git clone https://github.com/LUCASRENAA/Luner.git
cd Luner
sudo apt-get install libpq-dev python3-dev
sudo pip install psycopg2
pip3 install -r requirements.txt 
python3 manage.py migrate
python3 manage.py createsuperuser 
python3 manage.py runserver
```

