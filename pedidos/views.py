# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Usuario
from pedidos.models import Pedido, Cliente, EstadoPago, EstadoPedido
from productos.models import Producto, ProductoMedida, Medida, EstadoProducto, CategoriaMedida
from django.shortcuts import render, redirect
from productos.forms import ProductoFormSet, ProductoMedidaFormSet, ProductoMedidaForm, ProductoEditarFormSet, ProductoMedidaEditarFormSet
from collections import defaultdict
from django.contrib import messages
# -----------------------------------------------------------------
# LISTAR PRODUCTOS

def medida_choices():
    medida_choices = []
    for categoria in CategoriaMedida.objects.prefetch_related('medida_set'):
        opciones = [
            (medida.id, f"{medida.nombre} ({medida.unidad})")
            for medida in categoria.medida_set.all()
        ]
        medida_choices.append((categoria.nombre, opciones))
    return medida_choices
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

                cliente = Cliente.objects.get_or_create(
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

                    messages.success(request, f'Pedido {pedido.id} creado exitosamente.')
                    return redirect("listado_pedidos")
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
def editar_pedido(request, id):
    if request.session.get("estado_sesion"):
        pedido = Pedido.objects.select_related('estado_pedido', 'estado_pago', 'cliente', 'usuario').prefetch_related('pedidos').get(pk=id)
        if request.method == 'POST':
        # Actualizar cliente
            cliente = pedido.cliente
            cliente.nombre = request.POST['nombre']
            cliente.apellido = request.POST['apellido']
            cliente.correo = request.POST['correo']
            cliente.telefono = request.POST['telefono']
            cliente.save()


            # Actualizar pedido
            pedido.fecha_entrega = request.POST['fecha_entrega']
            pedido.subtotal = request.POST['subtotal']
            pedido.abono = request.POST['abono']

            pedido.estado_pago = EstadoPago.objects.get(pk=request.POST['estado_pago'])
            pedido.estado_pedido = EstadoPedido.objects.get(pk=request.POST['estado_pedido'])
            pedido.save()

            # Actualizar productos
            producto_formset = ProductoFormSet(request.POST, queryset=pedido.pedidos.all())
            if producto_formset.is_valid():
                productos = producto_formset.save(commit=False)
                for producto in productos:
                    producto.pedido = pedido
                    producto.save()

                    # Medidas por producto
                    medida_prefix = f'producto-{producto.id}-medidas'
                    for key in request.POST:
                        if key.startswith(medida_prefix) and key.endswith('-medidas'):
                            medida_index = key.split('-')[2]
                            medida_id = request.POST.get(f'{medida_prefix}-{medida_index}-medidas')
                            longitud = request.POST.get(f'{medida_prefix}-{medida_index}-longitud')
                            if medida_id and longitud:
                                medida_obj = Medida.objects.get(pk=medida_id)
                                ProductoMedida.objects.update_or_create(
                                    producto=producto,
                                    medidas=medida_obj,
                                    defaults={'longitud': longitud}
                                )
            messages.success(request, "Pedido actualizado correctamente.")
            return redirect('listado_pedidos')

        else:
            producto_formset = ProductoEditarFormSet(queryset=pedido.pedidos.all())
            medida_formsets = []
            for producto in pedido.pedidos.all():
                medida_form = ProductoMedidaEditarFormSet(instance=producto)
                medida_formsets.append(medida_form)
            for m in medida_formsets:
                print(m)
            estados_pago = EstadoPago.objects.all()
            estados_pedido = EstadoPedido.objects.all()
            estados_producto = EstadoProducto.objects.all()
            categorias_medida = medida_choices()
            datos = {
                "pedido": pedido,
                "nombre_usuario": request.session.get("nombre_usuario").upper(),
                'formset': producto_formset,
                'medida_formsets': medida_formsets,
                'medida_form': medida_form,
                "estados_pedido": estados_pedido,
                "estados_pago": estados_pago,
                "estados_producto": estados_producto,
                "categorias_medida": categorias_medida
            }
            return render(request, "editar_pedido.html", datos)
    else:
        messages.error(request, 'Debe iniciar sesión para ingresar a la página.')
        redirect('login')

# -----------------------------------------------------------------
# CAMBIAR ESTADO PEDIDO
def cambiar_estado_pedido(request, id):
    if request.session.get("estado_sesion"):
        pedido = Pedido.objects.get(pk=id).select_related('estado_pedido', 'estado_pago', 'cliente', 'usuario').prefetch_related('pedidos')
        datos = {
            "pedido": pedido,
            "nombre_usuario": request.session.get("nombre_usuario").upper()
        }
        return render(request, "editar_pedido.html", datos)
    else:
        return render(request, "main/index.html", {"r2": "Debe iniciar sesión para ingresar a la página."})
    # template que facilita el seguimiento de un pedido

# -----------------------------------------------------------------
# ELIMINAR PEDIDO
def eliminar_pedido(request, id):
    if request.session.get('estado_sesion'):
        pedido = Pedido.objects.get(pk=id)
        pedido.delete()
        messages.success(request, f'Pedido {id} eliminado exitosamente.')
        return redirect("listado_pedidos")
    else:
        messages.error(request, 'Debe iniciar sesión para ingresar a la página.')
        redirect('login')