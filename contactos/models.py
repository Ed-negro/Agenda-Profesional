from django.db import models

class Contacto(models.Model):
    # Campos principales (Nombre y correo obligatorio según los criterios de aceptación)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    
    # Detalles del perfil (enlaces a LinkedIn, GitHub y habilidades) [cite: 7]
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)
    habilidades = models.TextField(help_text="Lista corta de habilidades separadas por comas")

    def __str__(self):
        return self.nombre
