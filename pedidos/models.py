from django.db import models
from main.models import Usuario

class EstadoPedido(models.Model):
    nombre = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class EstadoPago(models.Model):    
    nombre = models.CharField(max_length=20, blank=False, null=False)
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=50, blank=False, null=False)
    correo = models.CharField(max_length=100, blank=False, null=False, unique=True)
    telefono = models.CharField(max_length=9, blank=False, null=False)

    def __str__(self):
        return self.correo
    
class Pedido(models.Model):
    fecha_pedido = models.DateTimeField(auto_now=True, blank=False, null=False)
    fecha_entrega = models.DateTimeField(blank=False, null=False)
    subtotal = models.PositiveIntegerField(blank=False, null=False)
    abono = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarios')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='clientes')
    estado_pedido = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE, related_name='estados_pedidos')
    estado_pago = models.ForeignKey(EstadoPago, on_delete=models.CASCADE, related_name='estados_pagos')


    def __str__(self):
        return f"Pedido para: {self.cliente.nombre} "