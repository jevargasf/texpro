# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Usuario
from pedidos.models import Pedido, Cliente
from productos.models import Producto, ProductoMedida, Medida, EstadoProducto, CategoriaMedida
from django.shortcuts import render, redirect
from productos.forms import ProductoFormSet, ProductoMedidaFormSet, ProductoMedidaForm
from collections import defaultdict

# -----------------------------------------------------------------
# LISTAR PRODUCTOS
def mostrar_listado_pedidos(request):
    if request.session.get("estado_sesion"):
        pedidos = Pedido.objects.all().select_related("estado_pedido", "estado_pago", "cliente", "usuario").prefetch_related("pedidos")
        datos = {
            "pedidos": pedidos,
            "nombre_usuario": request.session.get("nombre_usuario").upper()
        }
        return render(request, "pedidos.html", datos)
    else:
        return render(request, "main/index.html", {"r2": "Debe iniciar sesión para ingresar a la página."})

# -----------------------------------------------------------------
# CREAR PEDIDO

def crear_pedido(request):
    if request.session.get('estado_sesion'):
        print(request.method)
        medida_choices = []
        for categoria in CategoriaMedida.objects.prefetch_related('medida_set'):
            opciones = [
                (medida.id, f"{medida.nombre} ({medida.unidad})")
                for medida in categoria.medida_set.all()
            ]
            medida_choices.append((categoria.nombre, opciones))
        if request.method == 'POST':
            try:
                # Datos del cliente y pedido
                fecha = request.POST.get('fecha')
                nombre_cliente = request.POST.get('nombre')
                apellido_cliente = request.POST.get('apellido')
                correo = request.POST.get('correo')
                telefono = request.POST.get('telefono')
                usuario = Usuario.objects.get(pk=request.session.get('id_usuario'))

                # Crear cliente
                cliente = Cliente.objects.create(
                    nombre=nombre_cliente,
                    apellido=apellido_cliente,
                    correo=correo,
                    telefono=telefono
                )

                # Crear pedido
                pedido = Pedido.objects.create(
                    fecha_entrega=fecha,
                    usuario=usuario,
                    cliente=cliente
                )

                # Formset de productos
                producto_formset = ProductoFormSet(request.POST, queryset=Producto.objects.none())

                if producto_formset.is_valid():
                    productos = producto_formset.save(commit=False)

                    for i, producto in enumerate(productos):
                        producto.pedido = pedido
                        producto.save()

                    # Procesar medidas manualmente desde request.POST
                    medida_prefix = f'form-{i}-medidas'
                    medidas_producto = []

                    # Buscar todas las claves que empiezan con el prefijo
                    for key in request.POST:
                        if key.startswith(medida_prefix) and key.endswith('-medidas'):
                            # Extraer el índice de la medida
                            medida_index = key.split('-')[2]
                            medida_id = request.POST.get(f'{medida_prefix}-{medida_index}-medidas')
                            longitud = request.POST.get(f'{medida_prefix}-{medida_index}-longitud')

                            if medida_id and longitud:
                                try:
                                    medida_obj = Medida.objects.get(pk=medida_id)
                                    ProductoMedida.objects.create(
                                        producto=producto,
                                        medidas=medida_obj,
                                        longitud=longitud
                                    )
                                except Medida.DoesNotExist:
                                    continue  # ignorar si la medida no existe

                    return render(request, 'pedidos.html')
                else:
                    return render(request, 'crear_pedido.html', {
                        'formset': producto_formset,
                        'medida_choices': medida_choices,
                        'medida_form': ProductoMedidaForm(),
                        'r2': 'Error en los datos de los productos.'
                    })

            except Exception as e:
                return render(request, 'crear_pedido.html', {
                    'formset': ProductoFormSet(queryset=Producto.objects.none()),
                    'medida_choices': medida_choices,
                    'medida_form': ProductoMedidaForm(),
                    'r2': f'Error al crear el pedido: {str(e)}'
                })

        else:
            formset = ProductoFormSet(queryset=Producto.objects.none())
            medida_form = ProductoMedidaForm()  # solo uno como plantilla

            return render(request, 'crear_pedido.html', {
                'formset': formset,
                'medida_choices': medida_choices,
                'medida_form': medida_form
            })





    else:
        return redirect('login')




# -----------------------------------------------------------------
# ACTUALIZAR PEDIDO
def seguimiento_pedido(request):
    pass
    # template que facilita el seguimiento de un pedido

# -----------------------------------------------------------------
# ELIMINAR PEDIDO
def eliminar_pedido(request, pedido_id):
    if request.session.get('estado_sesion'):
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        pedido.delete()
        return redirect("listado_pedidos")
    else:
        return render(request, "index.html", {"r2": "Debe iniciar sesión para ingresar a la página."})


