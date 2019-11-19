#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: El 27 de c/mes antes de calcular nov. limpiar bd de nov.
import mysqlDAO
import csvDAO
from datetime import timedelta
import datetime as dt
import datedelta

DIA_CIERRE = 26
EXCEPCIONES = ['5365', '5366', '4164']

def fecha_inicio_novedades(tabla):
    '''
    Calculo la fecha de inicio para el ultimo periodo de novedades,
    teniendo en cuenta el dia de cierre.
    '''
    ultima_fecha_subida = mysqlDAO.fecha_mas_reciente(tabla)
    if ultima_fecha_subida is not None:
        return (ultima_fecha_subida + timedelta(days=1)).strftime('%Y-%m-%d')

    hoy = dt.date.today()
    inicio_novedades = hoy.replace(day=DIA_CIERRE)
    if hoy.day < DIA_CIERRE:
        inicio_novedades = inicio_novedades - datedelta.MONTH

    return inicio_novedades.strftime('%Y-%m-%d')

def fecha_fin_novedades():
    '''
    Calculo la fecha de fin para el ultimo periodo de novedades.
    '''
    fecha_hasta = dt.date.today() - timedelta(days=1)
    return fecha_hasta.strftime('%Y-%m-%d')

def diccionario_agenda(ingresos_presea):
    agenda = {}
    fechas = []
    fecha_agenda = dt.datetime.now() + timedelta(days=6)
    for _ in range(7):
        fecha_agenda = fecha_agenda + timedelta(days=1)
        fechas.append(fecha_agenda.strftime('%Y-%m-%d'))

        for legajo, dato in ingresos_presea.items():
            if legajo not in agenda.keys() and legajo not in EXCEPCIONES:
                agenda[legajo] = {
                'nombre': dato['nombre'],
                'puesto': dato['puesto'],
                'sucursal': dato['sucursal'],
                'provincia': dato['provincia'],
                'supervisor': dato['supervisor'],
                'zonal': dato['zonal'],
                'regional': dato['regional'],
                'lista_fechas': fechas
                }
    return agenda

def diccionario_novedades_oficina(sentencia):
    novedades_oficina = {}
    for tupla in sentencia:
        legajo = tupla[0].strip()
        if legajo is None:
            continue
        puesto = tupla[2]
        try:
            supervisor = tupla[3].strip()
        except:
            supervisor = ''
        try:
            zonal = tupla[4].strip()
        except:
            zonal = ''
        try:
            regional = tupla[5].strip()
        except:
            regional = ''
        sucursal = tupla[11]
        if ('OFICINA' not in sucursal or
            sucursal == 'OFICINA OPERACIONES VENTAS' or
            sucursal == 'OFICINA OPERACIONES LOGISTICA'):
            continue
        nombre = tupla[1]
        fecha = tupla[6]
        entrada_agenda = tupla[7].strip()
        entrada_agenda = normalizacion_hs_agenda(tupla[7].strip())
        entrada_fichaje = tupla[8].strip()
        entrada_fichaje = normalizacion_hs_fichaje(entrada_fichaje)
        estado_entrada = calcular_estados(entrada_agenda, entrada_fichaje, 'Entrada')
        salida_agenda = tupla[9].strip()
        salida_agenda = normalizacion_hs_agenda(salida_agenda)
        salida_fichaje = tupla[10].strip()
        salida_fichaje = normalizacion_hs_fichaje(salida_fichaje)
        estado_salida = calcular_estados(salida_agenda, salida_fichaje, 'Salida')
        if legajo not in novedades_oficina.keys():
            novedades_oficina[legajo] = {
                'datos': {
                    'nombre': nombre,
                    'supervisor': supervisor,
                    'zonal': zonal,
                    'regional': regional,
                    'puesto': puesto
                },
                'agenda': [{
                    'fecha': fecha,
                    'entrada_agenda': entrada_agenda,
                    'entrada_fichaje': entrada_fichaje,
                    'entrada_estado': estado_entrada,
                    'salida_agenda': salida_agenda,
                    'salida_fichaje': salida_fichaje,
                    'salida_estado': estado_salida
                }]
                }
        elif fecha not in novedades_oficina[legajo]['agenda']:
            novedades_oficina[legajo]['agenda'].append({
                    'fecha': fecha,
                    'entrada_agenda': entrada_agenda,
                    'entrada_fichaje': entrada_fichaje,
                    'entrada_estado': estado_entrada,
                    'salida_agenda': salida_agenda,
                    'salida_fichaje': salida_fichaje,
                    'salida_estado': estado_salida
                })
    return novedades_oficina

def diccionario_fichaje_oficina(archivo_escritorio_remoto):
    file_object = open(archivo_escritorio_remoto, 'r', encoding='ISO-8859-1')
    encabezado = file_object.readline()
    detalle_fichaje = file_object.readlines()
    fichaje_oficina = {}
    for linea in detalle_fichaje:
        valores = linea.split(',')
        legajo = valores[1]
        fecha_hora = valores[2].split()
        fecha = fecha_hora[0]
        hora = fecha_hora[1]
        hora = dt.datetime.strptime(hora, '%H:%M:%S').time()
        descripcion = valores[4]
        HorarioEntrada = dt.time(0, 0)
        HorarioSalida = dt.time(0, 0)
        # Si no corresponde a un legajo, descarto el registro
        if legajo == 'Berna':
            continue
        if descripcion == 'Malaver E':
            HorarioEntrada = hora
        else:
            HorarioSalida = hora
        # Si el legajo no esta, lo agregamos creando un nuevo diccionario
        if legajo not in fichaje_oficina.keys():
            fichaje_oficina[legajo] = {fecha: [HorarioEntrada,
                                               HorarioSalida]}
        else:
            if fecha not in fichaje_oficina[legajo]:
                dictFechas = fichaje_oficina[legajo]
                dictFechas[fecha] = [HorarioEntrada, HorarioSalida]
            else:
                dictFechas = fichaje_oficina[legajo]
                listaHoras = dictFechas[fecha]
                if HorarioEntrada != dt.time(0, 0):
                    if listaHoras[0] == dt.time(0, 0):
                        listaHoras[0] = HorarioEntrada
                    elif HorarioEntrada < listaHoras[0]:
                        listaHoras[0] = HorarioEntrada
                if HorarioSalida > listaHoras[1]:
                    listaHoras[1] = HorarioSalida
    file_object.close()
    return fichaje_oficina

def normalizacion_hs_agenda(variable):
    try:
        variable = dt.datetime.strptime(variable.strip(), '%H:%M').time()
        return variable
    except:
        if variable is None or variable == '':
            variable = '00:00:00'
            variable = dt.datetime.strptime(variable, '%H:%M:%S').time()
            return variable
        else:
            return variable

def normalizacion_hs_fichaje(variable):
    try:
        variable = dt.datetime.strptime(variable.strip(), '%H:%M:%S').time()
        return variable
    except:
        variable = '00:00:00'
        variable = dt.datetime.strptime(variable, '%H:%M:%S').time()
        return variable

def calcular_estados(agenda, fichaje, entrada_salida):
    # Agenda vacia
    if agenda is None or agenda == dt.time(0, 0):
        if fichaje is None or fichaje == dt.time(0, 0):
            return 'No agenda - No fichaje'
        else:
            return 'No agenda'

    # Fichaje vacio
    if isinstance(agenda, dt.time) and (fichaje is None or fichaje == '' or fichaje == dt.time(0, 0)):
        return 'No fichaje'

    # Agenda tiene un time != 00:00
    if isinstance(agenda, dt.time):
        if entrada_salida == 'Entrada':
            ENTRADA_TOLERANCIA = 3
            entrada_retraso = dt.time(agenda.hour, agenda.minute + 3)
            if fichaje <= entrada_retraso:
                return 'Correcto'
            else:
                return 'Tarde'
        elif entrada_salida == 'Salida':
            SALIDA_TOLERANCIA = 30
            minutos = (agenda.minute + SALIDA_TOLERANCIA)%60
            horas = agenda.hour + (agenda.minute + SALIDA_TOLERANCIA)//60
            salida_retraso = dt.time(horas, minutos)
            if fichaje < agenda:
                return 'Retiro anticipado'
            elif fichaje < salida_retraso:
                return 'Correcto'
            else:
                # TODO: Verificar horas extras
                return 'Sobretiempo'


    # 2 - El resto de las opciones

    # Agenda es un string
    opciones_agenda = [
        # opciones licencia
        'art',
        'licencia deportiva',
        'enfermedad',
        'enfermedad familiar',
        'excedencia',
        'injustificada',
        'licencia gremial',
        'maternidad',
        'matrimonio',
        'permiso gremial',
        'reserva de puesto',
        'sin goce de sueldo',
        # opciones agenda
        'accion movil',
        'franco',
        'home office',
        'trabajo fuera de oficina',
        # vacaciones
        'vacaciones',
        'vacaciones jefes',
        'no ficha', # eliminar esta opciones
        ]
    if agenda.lower() not in opciones_agenda:
        raise Exception('Opcion agenda no valida: ' + agenda)

    if fichaje is None or fichaje == '' or fichaje == dt.time(0, 0, 0):
        return 'Correcto'
    else:
        return agenda + ' y se registro ' + entrada_salida

def diccionario_fichaje_eaya(query):
    fichaje_eaya = {}
    for tupla in query:
        ingreso = dt.timedelta(0)
        salida = dt.timedelta(0)
        legajo = tupla[1]
        fecha = tupla[7]
        hora = tupla[8]
        descripcion = tupla[5]
        if descripcion == 'Ingreso':
            ingreso = hora
        elif descripcion == 'Salida':
            salida = hora
        if legajo not in fichaje_eaya.keys():
            fichaje_eaya[legajo] = {fecha: [ingreso, salida]}
        # Si el legajo esta y tambien la fecha, verifico y modifico la hora
        elif fecha in fichaje_eaya[legajo].keys():
            dictFechas = fichaje_eaya[legajo]
            listaHoras = dictFechas[fecha]
            if ingreso != dt.timedelta(0):
                if listaHoras[0] != dt.timedelta(0):
                    if ingreso < listaHoras[0]:
                        listaHoras[0] = ingreso
                else:
                    listaHoras[0] = ingreso
            if salida != dt.timedelta(0):
                if listaHoras[1] != dt.timedelta(0):
                    if salida > listaHoras[1]:
                        listaHoras[1] = salida
                else:
                    listaHoras[1] = salida
        # El legajo esta y tengo una nueva fecha, agrego la fecha y horas
        else:
            dictFechas = fichaje_eaya[legajo]
            dictFechas[fecha] = [ingreso, salida]
    return fichaje_eaya

def diccionario_novedades_eaya(query):
    novedades_eaya = {}
    for tupla in query:
        nombre = tupla[1]
        legajo = tupla[0]
        if legajo is None:
            continue
        puesto = tupla[2]
        sucursal = tupla[3]
        if 'OFICINA' in sucursal:
            continue
        try:
            supervisor = tupla[5].strip()
        except:
            supervisor = ''
        try:
            zonal = tupla[6].strip()
        except:
            zonal = ''
        try:
            regional = tupla[7].strip()
        except:
            regional = ''
        fecha = tupla[8]
        entrada_agenda = tupla[9]
        entrada_agenda = normalizacion_hs_agenda(entrada_agenda)
        entrada_fichaje = tupla[10]
        if entrada_fichaje is None:
            entrada_fichaje = dt.time(0, 0)
        else:
            entrada_fichaje = (dt.datetime.min + entrada_fichaje).time()
        estado_entrada = calcular_estados(entrada_agenda, entrada_fichaje, 'Entrada')
        salida_agenda = tupla[11].strip().replace('\n', '')
        salida_agenda = normalizacion_hs_agenda(salida_agenda)
        salida_fichaje = tupla[12]
        if salida_fichaje is None:
            salida_fichaje = dt.time(0, 0)
        else:
            salida_fichaje = (dt.datetime.min + salida_fichaje).time()
        estado_salida = calcular_estados(salida_agenda, salida_fichaje, 'Salida')
        if legajo not in novedades_eaya.keys():
            novedades_eaya[legajo] = {
                'datos': {
                    'nombre': nombre,
                    'supervisor': supervisor,
                    'zonal': zonal,
                    'regional': regional,
                    'puesto': puesto
                },
                'agenda': [{
                    'fecha': fecha,
                    'entrada_agenda': entrada_agenda,
                    'entrada_fichaje': entrada_fichaje,
                    'entrada_estado': estado_entrada,
                    'salida_agenda': salida_agenda,
                    'salida_fichaje': salida_fichaje,
                    'salida_estado': estado_salida
                }]
                }
        elif fecha not in novedades_eaya[legajo]['agenda']:
            novedades_eaya[legajo]['agenda'].append({
                    'fecha': fecha,
                    'entrada_agenda': entrada_agenda,
                    'entrada_fichaje': entrada_fichaje,
                    'entrada_estado': estado_entrada,
                    'salida_agenda': salida_agenda,
                    'salida_fichaje': salida_fichaje,
                    'salida_estado': estado_salida
                })
    return novedades_eaya


if __name__ == '__main__':
    # PRUEBA CIERRE AUTOMATIZADO
    # mysqlDAO.historico_novedades()

    # INGRESOS
    ingresos = csvDAO.load_ingresos()
    ingresos_csv = csvDAO.dump_ingresos(ingresos)
    mysqlDAO.ingresos_mysql(ingresos_csv)

    #HORARIOS PRESTABLECIDOS
    # horarios_lic = csvDAO.load_horarios_licencias()

    # AGENDA
    dict_agenda = diccionario_agenda(ingresos)
    archivo_agenda = csvDAO.dump_agenda(dict_agenda, horarios_lic)
    mysqlDAO.subir_agenda(archivo_agenda)

    # FICHAJE OFICINA
    # dicccionario_oficina = diccionario_fichaje_oficina('ema.csv')
    # archivo = csvDAO.dump_fichaje_oficina(dicccionario_oficina)
    # mysqlDAO.subir_fichaje('fichaje_oficina', archivo)


    # fecha_fin = fecha_fin_novedades()
    # NOVEDADES OFICINA
    # fecha_inicio = fecha_inicio_novedades('novedades_oficina')
    # fichaje_oficina = mysqlDAO.agenda_fichaje_oficina(fecha_inicio, fecha_fin)
    # dict_oficina = diccionario_novedades_oficina(fichaje_oficina)
    # novedades_oficina = csvDAO.dump_novedades_oficina(dict_oficina)
    # mysqlDAO.subir_tabla(novedades_oficina, 'novedades_oficina')

    # FICHAJE EAYA
    # fecha_inicio = fecha_inicio_novedades('novedades_eaya')
    # agenda_fichaje = mysqlDAO.fechas_fichaje_eaya(fecha_inicio, fecha_fin)
    # fichaje_eaya = diccionario_fichaje_eaya(agenda_fichaje)
    # archivo = csvDAO.dump_fichaje_eaya(fichaje_eaya)
    # mysqlDAO.subir_fichaje('fichaje_eaya', archivo)

    # NOVEDADES EAYA
    # fecha_inicio = fecha_inicio_novedades('novedades_eaya')
    # fichaje_eaya = mysqlDAO.agenda_fichaje_eaya(fecha_inicio, fecha_fin)
    # dict_eaya = diccionario_novedades_eaya(fichaje_eaya)
    # novedades_eaya = csvDAO.dump_novedades_eaya(dict_eaya)
    # mysqlDAO.subir_tabla(novedades_eaya, 'novedades_eaya')
