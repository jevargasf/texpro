from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=50, blank=False, null=False)
    correo = models.CharField(max_length=100, blank=False, null=False, unique=True)
    contrasena = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.correo