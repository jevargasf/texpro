# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Usuario
from pedidos.models import Pedido, EstadoPago, EstadoPedido, Cliente
from productos.models import Producto, ProductoMedida, Medida, EstadoProducto

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
# CREAR PRODUCTO
def mostrar_form_reg_producto(request):
    if request.session.get("estado_sesion"):
        if request.method == "POST":
            nombre = request.POST["nombre"]
            descripcion = request.POST.get("descripcion", "")
            precio_unitario = int(request.POST["precio_unitario"])
            cantidad = int(request.POST["cantidad"])
            estado_producto = EstadoProducto.objects.get(pk=request.POST["estado_producto"])

            producto = Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio_unitario=precio_unitario,
                cantidad=cantidad,
                estado_producto=estado_producto
            )

            # Opcional: asociar medidas al producto
            if "medida" in request.POST and request.POST["medida"] and request.POST["longitud"]:
                medida = Medida.objects.get(pk=request.POST["medida"])
                longitud = int(request.POST["longitud"])
                ProductoMedida.objects.create(
                    producto=producto,
                    medidas=medida,
                    longitud=longitud
                )

            return redirect("listado_productos")

        else:
            datos = {
                "estados_producto": EstadoProducto.objects.all(),
                "medidas": Medida.objects.all(),
                "nombre_usuario": request.session.get("nombre_usuario").upper()
            }
            return render(request, "productos/form_reg.html", datos)
    else:
        return render(request, "index.html", {"r2": "Debe iniciar sesión para ingresar a la página."})


# -----------------------------------------------------------------
# ACTUALIZAR PRODUCTO
def mostrar_form_act_producto(request, producto_id):
    if request.session.get("estado_sesion"):
        producto = get_object_or_404(Producto, pk=producto_id)

        if request.method == "POST":
            producto.nombre = request.POST["nombre"]
            producto.descripcion = request.POST.get("descripcion", "")
            producto.precio_unitario = int(request.POST["precio_unitario"])
            producto.cantidad = int(request.POST["cantidad"])
            producto.estado_producto = EstadoProducto.objects.get(pk=request.POST["estado_producto"])
            producto.save()

            return redirect("listado_productos")

        else:
            datos = {
                "producto": producto,
                "estados_producto": EstadoProducto.objects.all(),
                "medidas": Medida.objects.all(),
                "nombre_usuario": request.session.get("nombre_usuario").upper()
            }
            return render(request, "productos/form_act.html", datos)
    else:
        return render(request, "index.html", {"r2": "Debe iniciar sesión para ingresar a la página."})


# -----------------------------------------------------------------
# ELIMINAR PRODUCTO
def eliminar_producto(request, producto_id):
    if request.session.get("estado_sesion"):
        producto = get_object_or_404(Producto, pk=producto_id)
        producto.delete()
        return redirect("listado_productos")
    else:
        return render(request, "index.html", {"r2": "Debe iniciar sesión para ingresar a la página."})
    


# -----------------------------------------------------------------
# CREAR PEDIDO
def mostrar_form_reg_pedido(request):
    if request.session.get('estado_sesion'):
        if request.method == "POST":
            cliente_id = request.POST["cliente"]
            estado_pedido_id = request.POST["estado_pedido"]
            estado_pago_id = request.POST["estado_pago"]

            cliente = Cliente.objects.get(pk=cliente_id)
            estado_pedido = EstadoPedido.objects.get(pk=estado_pedido_id)
            estado_pago = EstadoPago.objects.get(pk=estado_pago_id)
            usuario = Usuario.objects.get(pk=request.session.get("id_usuario"))

            Pedido.objects.create(
                fecha_entrega=request.POST["fecha_entrega"],
                subtotal=int(request.POST["subtotal"]),
                abono=int(request.POST.get("abono", 0)),
                usuario=usuario,
                cliente=cliente,
                estado_pedido=estado_pedido,
                estado_pago=estado_pago
            )

            return redirect("listado_pedidos")
        else:
            datos = {
                "clientes": Cliente.objects.all(),
                "estados_pedido": EstadoPedido.objects.all(),
                "estados_pago": EstadoPago.objects.all(),
                "nombre_usuario": request.session.get("nombre_usuario").upper()
            }
            return render(request, "pedidos/form_reg.html", datos)
    else:
        return render(request, "index.html", {"r2": "Debe iniciar sesión para ingresar a la página."})


# -----------------------------------------------------------------
# ACTUALIZAR PEDIDO
def mostrar_form_act_pedido(request, pedido_id):
    if request.session.get('estado_sesion'):
        pedido = get_object_or_404(Pedido, pk=pedido_id)

        if request.method == "POST":
            pedido.fecha_entrega = request.POST["fecha_entrega"]
            pedido.subtotal = int(request.POST["subtotal"])
            pedido.abono = int(request.POST.get("abono", 0))

            pedido.cliente = Cliente.objects.get(pk=request.POST["cliente"])
            pedido.estado_pedido = EstadoPedido.objects.get(pk=request.POST["estado_pedido"])
            pedido.estado_pago = EstadoPago.objects.get(pk=request.POST["estado_pago"])
            pedido.save()

            return redirect("listado_pedidos")
        else:
            datos = {
                "pedido": pedido,
                "clientes": Cliente.objects.all(),
                "estados_pedido": EstadoPedido.objects.all(),
                "estados_pago": EstadoPago.objects.all(),
                "nombre_usuario": request.session.get("nombre_usuario").upper()
            }
            return render(request, "pedidos/form_act.html", datos)
    else:
        return render(request, "index.html", {"r2": "Debe iniciar sesión para ingresar a la página."})


# -----------------------------------------------------------------
# ELIMINAR PEDIDO
def eliminar_pedido(request, pedido_id):
    if request.session.get('estado_sesion'):
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        pedido.delete()
        return redirect("listado_pedidos")
    else:
        return render(request, "index.html", {"r2": "Debe iniciar sesión para ingresar a la página."})


