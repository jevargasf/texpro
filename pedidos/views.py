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

                        # Procesar medidas para este producto
                        medida_prefix = f'form-{i}-medidas'
                        medida_formset = ProductoMedidaFormSet(
                            request.POST,
                            instance=producto,
                            prefix=medida_prefix
                        )

                        if medida_formset.is_valid():
                            medida_formset.save()
                        else:
                            return render(request, 'crear_pedido.html', {
                                'formset': producto_formset,
                                'error': f'Error en medidas del producto {producto.nombre}'
                            })

                    return redirect('detalle_pedido', pedido_id=pedido.id)

                else:
                    return render(request, 'crear_pedido.html', {
                        'formset': producto_formset,
                        'error': 'Error en los datos de los productos.'
                    })

            except Exception as e:
                return render(request, 'crear_pedido.html', {
                    'formset': ProductoFormSet(queryset=Producto.objects.none()),
                    'error': f'Error al crear el pedido: {str(e)}'
                })

        else:


            medida_choices = {}
            for categoria in CategoriaMedida.objects.prefetch_related('medida_set'):
                medida_choices[categoria.nombre] = [
                    (medida.id, f"{medida.nombre} ({medida.unidad})")
                    for medida in categoria.medida_set.all()
                ]

            formset = ProductoFormSet(queryset=Producto.objects.none())
            return render(request, 'crear_pedido.html', {
                'formset': formset,
                'medida_choices': medida_choices
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


