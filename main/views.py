from django.shortcuts import render, redirect
from main.models import Usuario
# Create your views here.

def mostrar_index(request):
    estado_sesion = request.session.get('estado_sesion')
    if estado_sesion is True:
        datos = {
            'nombre_usuario': request.session.get('nombre_usuario')
        }
        return render(request, "index.html", datos)
    else:
        datos = {
            'r2': 'Debe iniciar sesión para ingresar a la página.'
        }
        return redirect('login')

def registrar_usuario(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        contrasena = request.POST['contrasena']

        nuevo_usuario = Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contrasena=contrasena
        )
        nuevo_usuario.save()
        datos = {
            'r2': 'Usuario creado correctamente. Por favor, inicie sesión.'
        }
        return render(request, "login.html", datos)

def login_usuario(request):
    if request.method == 'POST':
        correo = request.POST['txtcorreo']
        con = request.POST['txtcon']
        usuario_consulta = Usuario.objects.filter(correo=correo, contrasena=con).values()
        if usuario_consulta:
            usuario_login = Usuario.objects.get(correo=correo)
            request.session['estado_sesion'] = True
            request.session['id_usuario'] = usuario_consulta[0]['id']
            request.session['nombre_usuario'] = usuario_login.nombre.upper()

            datos = {
                'nombre_usuario': usuario_login.nombre.upper()
            }

            return redirect('index')
        else:
            datos = {
                'r2': 'Usuario y/o contraseña incorrectos. Intente nuevamente.'
            }
            return render(request, "login.html", datos)
    else:
        datos = {
            'r2': 'No se pudo procesar la solicitud.'
        }
        return render(request, "login.html", datos)

def cerrar_sesion(request):
    try:
        del request.session["estado_sesion"]
        del request.session["id_usuario"]
        del request.session["nombre_usuario"]
        
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')