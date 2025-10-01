from django.contrib import admin
from main.models import Usuario

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    pass

admin.site.register(Usuario, UsuarioAdmin)