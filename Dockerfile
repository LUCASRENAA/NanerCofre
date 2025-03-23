FROM python:3.9-slim
LABEL mainteiner="Lucas Meira < LUCASRENAA at lucasrenaa1996@gmail.com>"

#Prevents Python from writing pyc files to disc
#Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
        && apt-get install -y nmap wget postgresql-client libpq-dev python3-dev build-essential \
        && wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - \
        && echo "deb https://aquasecurity.github.io/trivy-repo/deb jammy main" | tee -a /etc/apt/sources.list.d/trivy.list \
        && apt-get update && apt-get install -y trivy \
        && rm -rf /var/lib/apt/lists/*
        
WORKDIR /code/

COPY requirements.txt /code/

RUN pip3 install -U pip setuptools wheel &&\
        pip3 install -r  /code/requirements.txt

COPY . .

# Define uma variável de ambiente
ENV SECRET_KEY="teste"


CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]