import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cofre.settings")
django.setup()

User = get_user_model()

username = "admin3"
email = "admin2@example.com"
#tenho que tirar isso depois.
password = "senhaaleatoria"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuário criado!")
else:
    print("Superusuário já existe.")