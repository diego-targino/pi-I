<<<<<<< HEAD
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    estado = models.CharField(max_length=50, blank=True)
    cidade = models.CharField(max_length=50, blank=True)
    localidade = models.CharField(max_length=100, blank=True)
    fazenda = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome
=======
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
>>>>>>> a25b68c5809fd1d7ab5a6636f44fb6e370397478
