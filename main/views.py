from django.shortcuts import render, redirect
from main.models import Usuario
from django.contrib import messages
from pedidos.models import Pedido
# Create your views here.

def mostrar_index(request):
    estado_sesion = request.session.get('estado_sesion')
    if estado_sesion is True:
        recepcionados = Pedido.objects.filter(estado_pedido=1).count()
        en_proceso = Pedido.objects.filter(estado_pedido=2).count()
        listos_para_retiro = Pedido.objects.filter(estado_pedido=3).count()
        entregados = Pedido.objects.filter(estado_pedido=4).count()
        datos = {
            'nombre_usuario': request.session.get('nombre_usuario'),
            'recepcionados': recepcionados,
            'en_proceso': en_proceso,
            'listos_para_retiro': listos_para_retiro,
            'entregados': entregados
        }
        return render(request, "index.html", datos)
    else:
        messages.error(request, 'Debe iniciar sesión para ingresar a la página.')
        return redirect('login')

def registrar_usuario(request):
    try:
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
            messages.success(request, 'Usuario creado correctamente. Por favor, inicie sesión')
            return render(request, "login.html")
        else:
            return render(request, 'registrar.html')
    except Exception as e:
        messages.error(request, e)
        return render(request, 'registrar.html')

    
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
        return render(request, "login.html")

def cerrar_sesion(request):
    try:
        del request.session["estado_sesion"]
        del request.session["id_usuario"]
        del request.session["nombre_usuario"]
        
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')
    
def mostrar_quienes_somos(request):
    return render(request, 'quienes_somos.html')

def mostrar_conoce_texpro(request):
    return render(request, 'descripcion_texpro.html')

def mostrar_contacto(request):
    return render(request, 'contacto.html')
