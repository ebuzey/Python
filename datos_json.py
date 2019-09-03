#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

def cargar_datos(nombre_archivo):
    fo = open(nombre_archivo, 'r')
    return json.load(fo)

def listar_empleados(datos):
    return datos['empleados']

def listar_precios(datos):
    return datos['precios']

def total_ventas(datos):
    empleados = listar_empleados(datos)
    ventas_totales = 0
    for empleado in empleados:
        ventas = empleado['ventas']
        for venta in ventas.values():
            ventas_totales = ventas_totales + venta
    return ventas_totales

def total_venta_producto(datos, producto):
    empleados = listar_empleados(datos)
    ventas_producto = 0
    for empleado in empleados:
        ventas = empleado['ventas']
        for prod, venta in ventas.items():
            if prod == producto.lower():
                ventas_producto = ventas_producto + venta
    return ventas_producto

def total_venta_empleado(datos, nombre):
    empleados = listar_empleados(datos)
    ventas_empleado = 0
    for empleado in empleados:
        if nombre.lower() == empleado['nombre'].lower():
            ventas = empleado['ventas']
            for venta in ventas.values():
                ventas_empleado = ventas_empleado + venta
    return ventas_empleado

def monto_total_empleado(datos, nombre):
    empleados = listar_empleados(datos)
    precios = listar_precios(datos)
    total = 0
    for empleado in empleados:
        nombre_empleado = empleado['nombre']
        if nombre_empleado.lower() == nombre.lower():
            ventas = empleado['ventas']
            total = 0
            for prod, venta in ventas.items():
                total += venta * precios[prod]
            return total
    return None

def monto_total_productos(datos):
    precios = listar_precios(datos)
    empleados = listar_empleados(datos)
    ventas_totales = {}
    for empleado in empleados:
        ventas = empleado['ventas']
        for prod, venta in ventas.items():
            if prod not in ventas_totales.keys():
                ventas_totales[prod] = venta * precios[prod]
            else:
                ventas_totales[prod] += venta * precios[prod]
    return ventas_totales

def mayor_valor_diccionario(diccionario):
    mayor_valor = max(diccionario.values())
    mayores_claves = []
    for clave, valor in diccionario.items():
        if valor == mayor_valor:
            mayores_claves.append(clave)

    return mayores_claves, mayor_valor

def producto_mayor_facturacion(datos):
    montos = monto_total_productos(datos)
    return mayor_valor_diccionario(montos)

def producto_mas_vendido(datos):
    ventas = {}
    for prod in listar_precios(datos).keys():
        ventas[prod] = total_venta_producto(datos, prod)
    return mayor_valor_diccionario(ventas)



if __name__ == '__main__':
    datos = cargar_datos('datos.json')
    ventas = total_ventas(datos)
    vta_prod = total_venta_producto(datos, 'MOUSE')
    vta_empleado = total_venta_empleado(datos, 'BOB')
    precios = listar_precios(datos)
    monto_empleado = monto_total_empleado(datos, 'Bob')
    monto_productos = monto_total_productos(datos)
    mayor_facturacion = producto_mayor_facturacion(datos)
    mas_vendido = producto_mas_vendido(datos)
    # print('Monto total empleado: ', monto_empleado)
    print(mas_vendido)
    # print('Producto mas facturado: ', facturado_mayor)
