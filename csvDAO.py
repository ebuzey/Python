#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

INGRESOS_CSV = 'INGRESOS.csv'
HORARIOS_CSV = 'horarios_licencias.csv'
LICENCIAS_CSV = 'AUSENTISMO'

def load_ingresos():
    archivo_ingresos = open(INGRESOS_CSV, 'r', encoding='utf-8')
    encabezado = archivo_ingresos.readline()
    registros = archivo_ingresos.readlines()
    ingresos = {}
    for linea in registros:
        valores = linea.split(';')
        legajo = valores[0].strip()
        apellido = valores[1].strip()
        nombre = valores[2].strip()
        apellido_nombre = apellido + ' ' + nombre
        ingreso = valores[3].strip()
        baja = valores[4].strip()
        usuaria = valores[5].strip()
        puesto = valores[6].strip()
        sucursal = valores[7].strip()
        provincia = valores[8].strip()
        supervisor = valores[9].strip().replace(',', '')
        zonal = valores[10].strip().replace(',', '')
        regional = valores[11].replace(',', '').replace('\n', '')
        if legajo not in ingresos.keys() and len(baja) == 0:
            ingresos[legajo] = {
            'nombre': apellido_nombre,
            'ingreso': ingreso,
            'baja': baja,
            'usuaria': usuaria,
            'puesto': puesto,
            'sucursal': sucursal,
            'provincia': provincia,
            'supervisor': supervisor,
            'zonal': zonal,
            'regional': regional}
    archivo_ingresos.close()
    return ingresos

def dump_ingresos(dicc_ingresos):
    fecha = datetime.datetime.now()
    fecha = fecha.strftime('%Y-%m-%d')
    archivo_ingresos = 'Ingresos ' + fecha + '.csv'
    file_ingresos = open(archivo_ingresos, 'w', encoding='utf-8')
    for legajo in dicc_ingresos:
        linea = legajo + ',' + dicc_ingresos[legajo]['nombre'] + ','
        linea += dicc_ingresos[legajo]['ingreso'] + ','
        linea += dicc_ingresos[legajo]['baja'] + ','
        linea += dicc_ingresos[legajo]['usuaria'] + ','
        linea += dicc_ingresos[legajo]['puesto'] + ','
        linea += dicc_ingresos[legajo]['sucursal'] + ','
        linea += dicc_ingresos[legajo]['provincia'] + ','
        linea += dicc_ingresos[legajo]['supervisor'] + ','
        linea += dicc_ingresos[legajo]['zonal'] + ','
        linea += dicc_ingresos[legajo]['regional'] + '\n'
        file_ingresos.write(linea)

    file_ingresos.close()
    return archivo_ingresos

def load_horarios_licencias():
    horarios = open(HORARIOS_CSV, 'r', encoding='utf-8')
    detalle_horarios = horarios.readlines()
    horario_preestablecido = {}
    for linea in detalle_horarios:
        valor = linea.split(';')
        legajo = valor[0].strip()
        ingreso_lunes = valor[1].strip()
        salida_lunes = valor[2].strip()
        ingreso_martes = valor[3].strip()
        salida_martes = valor[4].strip()
        ingreso_miercoles = valor[5].strip()
        salida_miercoles = valor[6].strip()
        ingreso_jueves = valor[7].strip()
        salida_jueves = valor[8].strip()
        ingreso_viernes = valor[9].strip()
        salida_viernes = valor[10].strip()
        ingreso_sabado = valor[11].strip()
        salida_sabado = valor[12].strip()
        ingreso_domingo = valor[13].strip()
        salida_domingo = valor[14].strip()
        if legajo not in horario_preestablecido.keys():
            horario_preestablecido[legajo] = [ingreso_lunes, salida_lunes,
            ingreso_martes, salida_martes,
            ingreso_miercoles,
            salida_miercoles,
            ingreso_jueves, salida_jueves,
            ingreso_viernes, salida_viernes,
            ingreso_sabado, salida_sabado,
            ingreso_domingo, salida_domingo]

    horarios.close()
    return horario_preestablecido

def dump_agenda(dicc_agenda, horarios_preestablecidos):
    fecha = datetime.datetime.now()
    fecha = fecha.strftime('%Y-%m-%d')
    archivo_agenda = 'Agenda ' + fecha + '.csv'
    file_object = open(archivo_agenda, 'w', encoding='utf-8')
    id = ''
    dia_semana = 0
    for legajo, fecha in dicc_agenda.items():
        for dia in range(0, len(dicc_agenda[legajo]['lista_fechas'])):
            linea = id + ',' + legajo + ','
            linea += dicc_agenda[legajo]['nombre'] + ','
            linea += dicc_agenda[legajo]['puesto'] + ','
            linea += dicc_agenda[legajo]['sucursal'] + ','
            linea += dicc_agenda[legajo]['provincia'] + ','
            linea += dicc_agenda[legajo]['supervisor'] + ','
            linea += dicc_agenda[legajo]['zonal'] + ','
            linea += dicc_agenda[legajo]['regional'] + ','
            linea += str(dicc_agenda[legajo]['lista_fechas'][dia]) + ','
            if legajo in horarios_preestablecidos.keys():
                linea += horarios_preestablecidos[legajo][dia_semana] + ','
                dia_semana += 1
                linea += horarios_preestablecidos[legajo][dia_semana] + '\n'
                dia_semana += 1
                if dia_semana == 14:
                    dia_semana = 0
            else:
                linea += '00:00' + ',' + '00:00' + '\n'
            file_object.write(linea)
    file_object.close()
    return archivo_agenda

def dump_fichaje_oficina(dicc_fichaje_oficina):
    fecha = datetime.datetime.now()
    fecha = fecha.strftime('%Y-%m-%d')
    archivo_oficina_fichaje = 'Fichaje_oficina ' + fecha + '.csv'
    file_object = open(archivo_oficina_fichaje, 'w', encoding='utf-8')
    for legajo, dictFechas in dicc_fichaje_oficina.items():
        for fecha, horarios in dictFechas.items():
            linea = legajo + ',' + fecha + ','
            linea += str(horarios[0]) + ',' + str(horarios[1]) + '\n'
            file_object.write(linea)
    file_object.close()
    return archivo_oficina_fichaje

def dump_novedades_oficina(dicc_novedades_oficina):
    fecha = datetime.datetime.now()
    fecha = fecha.strftime('%Y-%m-%d')
    archivo_novedades_oficina = 'Novedades_Oficina ' + fecha + '.csv'
    file_object = open(archivo_novedades_oficina, 'w', encoding='utf-8')
    id = ''
    for clave, valor in dicc_novedades_oficina.items():
        legajo = clave
        datos = valor['datos']
        fechas = valor['agenda']
        for fecha in fechas:
            # pegar conversion de fechas
            fecha['fecha'] = fecha['fecha'].strftime('%Y-%m-%d')
            if isinstance(fecha['entrada_agenda'], datetime.time):
                fecha['entrada_agenda'] = "{:%H:%M:%S}".format(fecha['entrada_agenda'])
            if isinstance(fecha['entrada_fichaje'], datetime.time):
                fecha['entrada_fichaje'] = "{:%H:%M:%S}".format(fecha['entrada_fichaje'])
            if isinstance(fecha['entrada_agenda'], datetime.time):
                fecha['entrada_agenda'] = "{:%H:%M:%S}".format(fecha['entrada_agenda'])
            if isinstance(fecha['salida_agenda'], datetime.time):
                fecha['salida_agenda'] = "{:%H:%M:%S}".format(fecha['salida_agenda'])
            if isinstance(fecha['salida_fichaje'], datetime.time):
                fecha['salida_fichaje'] = "{:%H:%M:%S}".format(fecha['salida_fichaje'])
            if fecha['entrada_estado'] == 'Correcto' and fecha['salida_estado'] == 'Correcto':
                continue
            linea = (
                id,
                legajo,
                datos['nombre'],
                fecha['fecha'],
                fecha['entrada_agenda'],
                fecha['entrada_fichaje'],
                fecha['entrada_estado'],
                fecha['salida_agenda'],
                fecha['salida_fichaje'],
                fecha['salida_estado'],
                '', # Motivo Entrada
                '', # Motivo Salida
                'NO JUSTIFICA', # justifica
                '', # observaciones
                '', # justifica VH
                datos['supervisor'],
                datos['zonal'],
                datos['regional'],
                datos['puesto'],
                '\n'
            )
            linea = ','.join(linea)
            file_object.write(linea)
    file_object.close()
    return archivo_novedades_oficina

def dump_fichaje_eaya(dicc_novedades_eaya):
    fecha_archivo = datetime.datetime.now()
    fecha_archivo = fecha_archivo.strftime('%Y-%m-%d')
    archivo_fichaje_eaya = 'Fichaje_Eaya ' + fecha_archivo + '.csv'
    file_object = open(archivo_fichaje_eaya, 'w', encoding='utf-8')
    id = ''
    for legajo, dictFechas in dicc_novedades_eaya.items():
        for fecha, horarios in dictFechas.items():
            linea = id + ',' + legajo + ',' + fecha.strftime("%Y-%m-%d")
            linea += ',' + str(horarios[0]) + ',' + str(horarios[1]) + '\n'
            file_object.write(linea)
    file_object.close()

    return archivo_fichaje_eaya

def dump_novedades_eaya(dicc_novedades_eaya):
    fecha_archivo = datetime.datetime.now()
    fecha_archivo = fecha_archivo.strftime('%Y-%m-%d')
    archivo_novedades_eaya = 'Novedades_Eaya ' + fecha_archivo + '.csv'
    file_object = open(archivo_novedades_eaya, 'w', encoding='utf8')
    id = ''
    for clave, valor in dicc_novedades_eaya.items():
        legajo = clave
        datos = valor['datos']
        fechas = valor['agenda']
        for fecha in fechas:
            if isinstance(fecha['fecha'], datetime.date):
                fecha['fecha'] = fecha['fecha'].strftime('%Y-%m-%d')
            if isinstance(fecha['entrada_agenda'], datetime.time):
                fecha['entrada_agenda'] = "{:%H:%M:%S}".format(fecha['entrada_agenda'])
            if isinstance(fecha['entrada_fichaje'], datetime.time):
                fecha['entrada_fichaje'] = "{:%H:%M:%S}".format(fecha['entrada_fichaje'])
            if isinstance(fecha['entrada_agenda'], datetime.time):
                fecha['entrada_agenda'] = "{:%H:%M:%S}".format(fecha['entrada_agenda'])
            if isinstance(fecha['salida_agenda'], datetime.time):
                fecha['salida_agenda'] = "{:%H:%M:%S}".format(fecha['salida_agenda'])
            if isinstance(fecha['salida_fichaje'], datetime.time):
                fecha['salida_fichaje'] = "{:%H:%M:%S}".format(fecha['salida_fichaje'])
            if fecha['entrada_estado'] == 'Correcto' and fecha['salida_estado'] == 'Correcto':
                continue
            linea = (
                id,
                legajo,
                datos['nombre'],
                fecha['fecha'],
                fecha['entrada_agenda'],
                fecha['entrada_fichaje'],
                fecha['entrada_estado'],
                fecha['salida_agenda'],
                fecha['salida_fichaje'],
                fecha['salida_estado'],
                '', # motivo de entrada
                '', # motivo salida
                'NO JUSTIFICA', # justifica
                '', # observaciones
                datos['supervisor'],
                datos['zonal'],
                datos['regional'],
                datos['puesto'],
                '\n'
            )
            linea = ','.join(linea)
            file_object.write(linea)
    file_object.close()
    return archivo_novedades_eaya
