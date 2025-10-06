# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Usuario
from pedidos.models import Pedido, Cliente, EstadoPago, EstadoPedido
from productos.models import Producto, ProductoMedida, Medida, EstadoProducto, CategoriaMedida
from django.shortcuts import render, redirect
from productos.forms import ProductoFormSet, ProductoMedidaFormSet, ProductoMedidaForm, ProductoEditarFormSet, ProductoMedidaEditarFormSet
from collections import defaultdict
from django.contrib import messages
from django.db.models import Prefetch
from django.utils import timezone
import datetime

# -----------------------------------------------------------------
# HELPERS
def medida_choices():
    medida_choices = []
    for categoria in CategoriaMedida.objects.prefetch_related('medida_set'):
        opciones = [
            (medida.id, f"{medida.nombre} ({medida.unidad})")
            for medida in categoria.medida_set.all()
        ]
        medida_choices.append((categoria.nombre, opciones))
    return medida_choices

def convertir_fecha_aware(fecha_naive):
    fecha_naive = datetime.datetime(2025, 10, 9, 18, 37)
    fecha_aware = timezone.make_aware(fecha_naive)
    return fecha_aware

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
# OBTENER PEDIDO
def obtener_pedido(request, id):
    if request.session.get("estado_sesion"):

        pedido = get_object_or_404(
            Pedido.objects.select_related(
                'estado_pedido', 'estado_pago', 'cliente', 'usuario'
            ).prefetch_related(
                Prefetch(
                    'pedidos',
                    queryset=Producto.objects.prefetch_related(
                        Prefetch(
                            'medidas_producto',
                            queryset=ProductoMedida.objects.select_related('medidas')
                        )
                    )
                )
            ), pk=id)
        datos = {
            "pedido": pedido,
            "nombre_usuario": request.session.get("nombre_usuario").upper()
        }
        return render(request, "detalle_pedido.html", datos)
    else:
        messages.error(request, 'Debe iniciar sesión para ingresar a la página.')
        redirect('login')
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

                # Crear o obtener cliente
                cliente, created = Cliente.objects.get_or_create(
                    correo=correo,
                    defaults={
                        'nombre': nombre_cliente,
                        'apellido': apellido_cliente,
                        'telefono': telefono
                    }
                )

                # Crear pedido
                pedido = Pedido.objects.create(
                    fecha_entrega=fecha,
                    usuario=usuario,
                    cliente=cliente  # ← usar directamente 'cliente', no 'cliente_obj'
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
                        medida_index = 0
                        # Buscar todas las claves que empiezan con el prefijo
                        while True:
                            medida_key = f'{medida_prefix}-{medida_index}-medidas'
                            longitud_key = f'{medida_prefix}-{medida_index}-longitud'
                            
                            if medida_key not in request.POST:
                                break  # No hay más medidas para este producto
                                
                            medida_id = request.POST.get(medida_key)
                            longitud = request.POST.get(longitud_key)
                            
                            if medida_id and longitud:
                                try:
                                    medida_obj = Medida.objects.get(pk=medida_id)
                                    ProductoMedida.objects.create(
                                        producto=producto,
                                        medidas=medida_obj,
                                        longitud=longitud
                                    )
                                except Medida.DoesNotExist:
                                    pass  # Ignorar si la medida no existe
                            
                            medida_index += 1

                    messages.success(request, f'Pedido #{pedido.id} creado exitosamente.')
                    return redirect("listado_pedidos")
                else:
                    errores = producto_formset.errors
                    return render(request, 'crear_pedido.html', {
                        'formset': producto_formset,
                        'medida_choices': medida_choices,
                        'medida_form': ProductoMedidaForm(),
                        'r2': f'Error en los datos de los productos: {errores}'
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
            pedido.subtotal = request.POST.get('subtotal', 0) or 0
            pedido.abono = request.POST.get('abono', 0) or 0
            pedido.estado_pago = EstadoPago.objects.get(pk=request.POST['estado_pago'])
            pedido.estado_pedido = EstadoPedido.objects.get(pk=request.POST['estado_pedido'])
            pedido.save()

            # Actualizar productos usando el mismo patrón que crear_pedido
            producto_formset = ProductoEditarFormSet(request.POST, queryset=pedido.pedidos.all(), prefix='form')
            
            if producto_formset.is_valid():
            # Crear y procesar formsets de medidas por producto
                for i, form in enumerate(producto_formset.forms):
                    if form.cleaned_data.get('DELETE', False):
                        continue

                    producto = form.save(commit=False)
                    producto.pedido = pedido
                    producto.save()

                    medidas_formset = ProductoMedidaFormSet(
                        request.POST,
                        prefix=f'form-{i}-medidas',
                        instance=producto
                    )

                    if medidas_formset.is_valid():
                        medidas_formset.save()
                    else:
                        print(f"Errores en medidas del producto {i}:", medidas_formset.errors)

                messages.success(request, "Pedido actualizado correctamente.")
                return redirect('listado_pedidos')
            else:
                messages.error(request, f"Error en el formulario: {producto_formset.errors}")
                
        # GET request - mostrar formulario
        producto_formset = ProductoEditarFormSet(queryset=pedido.pedidos.all())
        
        # Preparar datos de medidas para cada producto
        formset_con_medidas = []
        for i, form in enumerate(producto_formset.forms):
            prefix = f'form-{i}-medidas'
            producto = form.instance
            medidas_formset = ProductoMedidaFormSet(
                prefix=prefix,
                instance=producto
            )
            formset_con_medidas.append((form, medidas_formset))


                
        estados_pago = EstadoPago.objects.all()
        estados_pedido = EstadoPedido.objects.all()
        estados_producto = EstadoProducto.objects.all()
        
        datos = {
            # En el contexto:
            'formset_con_medidas': formset_con_medidas,
            "pedido": pedido,
            "nombre_usuario": request.session.get("nombre_usuario").upper(),
            'formset': producto_formset,
            #'productos_con_medidas': productos_con_medidas,
            'medida_choices': medida_choices(),
            "estados_pedido": estados_pedido,
            "estados_pago": estados_pago,
            "estados_producto": estados_producto,
        }
        return render(request, "editar_pedido.html", datos)
    else:
        messages.error(request, 'Debe iniciar sesión para ingresar a la página.')
        return redirect('login')
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