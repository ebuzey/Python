#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector.constants import ClientFlag
import datetime as dt

# Conexion mysql - ENTORNO DE desarrollo
'''
mydb = mysql.connector.connect(
    host='',
    user='',
    passwd='',
    database='',
    allow_local_infile = 'True')
'''
# Conexion mysql
mydb = mysql.connector.connect(
    host='',
    user='',
    passwd='',
    database='',
    allow_local_infile = 'True')

if mydb.is_connected():
    print('Conexion a  establecida.')

mycursor = mydb.cursor()

def subir_tabla(archivo, tabla):
    query = "LOAD DATA LOCAL INFILE '" + archivo
    query += "' INTO TABLE " + tabla + " CHARACTER SET utf8 FIELDS "
    query += "TERMINATED BY ',';"
    mycursor.execute(query)
    mydb.commit()

def historico_novedades():
    hoy = dt.date.today()
    if hoy.day == 27:
        query_nov_eaya = 'INSERT INTO historico_nov_eaya (legajo, '
        query_nov_eaya += 'apellido_nombre, fecha, entrada_agenda, '
        query_nov_eaya += 'entrada_fichaje, estado_entrada, salida_agenda, '
        query_nov_eaya += 'salida_fichaje, estado_salida, motivo_entrada, '
        query_nov_eaya += 'motivo_salida, justifica, observacion, supervisor, '
        query_nov_eaya += 'zonal, regional, DescTrab) SELECT legajo, '
        query_nov_eaya += 'apellido_nombre, fecha, entrada_agenda, '
        query_nov_eaya += 'entrada_fichaje, estado_entrada, salida_agenda, '
        query_nov_eaya += 'salida_fichaje, estado_salida, motivo_entrada, '
        query_nov_eaya += 'motivo_salida, justifica, observacion, supervisor, '
        query_nov_eaya += 'zonal, regional, DescTrab FROM novedades_eaya'
        mycursor.execute(query_nov_eaya)
        mydb.commit()

        query_nov_eaya = 'TRUNCATE `novedades_eaya`'
        mycursor.execute(query_nov_eaya)
        mydb.commit()

        query_nov_oficina = 'INSERT INTO historico_nov_oficina (legajo, '
        query_nov_oficina += 'apellido_nombre, fecha, entrada_agenda, '
        query_nov_oficina += 'entrada_fichaje, estado_entrada, salida_agenda, '
        query_nov_oficina += 'salida_fichaje, estado_salida, motivo_entrada, '
        query_nov_oficina += 'motivo_salida, justifica, observaciones, '
        query_nov_oficina += 'justifica_vh, supervisor, zonal, regional, '
        query_nov_oficina += 'DescTrabajo) SELECT legajo, apellido_nombre, fecha, '
        query_nov_oficina += 'entrada_agenda, entrada_fichaje, estado_entrada, '
        query_nov_oficina += 'salida_agenda, salida_fichaje, estado_salida, '
        query_nov_oficina += 'motivo_entrada, motivo_salida, justifica, '
        query_nov_oficina += 'observaciones, justifica_vh, supervisor, zonal, '
        query_nov_oficina += 'regional, DescTrabajo FROM novedades_oficina'
        mycursor.execute(query_nov_oficina)
        mydb.commit()

        query_nov_oficina = 'TRUNCATE `novedades_oficina`'
        mycursor.execute(query_nov_oficina)
        mydb.commit()

def fecha_mas_reciente(tabla):
    if tabla != 'novedades_eaya' and tabla != 'novedades_oficina':
        raise ValueError('La tabla debe ser novedades_eaya o novedades_oficina')

    query = 'SELECT max(fecha) FROM ' + tabla
    mycursor.execute(query)
    fechas_nov = mycursor.fetchall()
    if fechas_nov == []:
        return None

    ultima_fecha_subida = fechas_nov[0][0]
    return ultima_fecha_subida

def agenda_fichaje_oficina(fecha_desde, fecha_hasta):
    sql_oficina = 'SELECT agenda.Legajo, agenda.Nombre, '
    sql_oficina += 'agenda.Puesto, ingresos.supervisor, '
    sql_oficina += 'ingresos.jefe_zonal, ingresos.jefe_reg, '
    sql_oficina += 'agenda.Fecha, agenda.HorarioEntrada, '
    sql_oficina += 'ifnull(fichaje_oficina.horario_entrada, "00:00:00") AS'
    sql_oficina += ' Horario_Entrada_Fichaje, agenda.HorarioSalida, '
    sql_oficina += 'ifnull(fichaje_oficina.horario_salida, "00:00:00") AS '
    sql_oficina += 'Horario_Salida_Fichaje, agenda.Sucursal FROM agenda '
    sql_oficina += 'LEFT JOIN fichaje_oficina ON agenda.Legajo = '
    sql_oficina += 'fichaje_oficina.legajo AND agenda.Fecha = '
    sql_oficina += 'fichaje_oficina.fecha LEFT JOIN ingresos ON agenda.Legajo '
    sql_oficina += '= ingresos.legajo WHERE agenda.Fecha BETWEEN ' + '"'
    sql_oficina += fecha_desde + '"' + ' and ' + '"' + fecha_hasta + '"' + ';'
    mycursor.execute(sql_oficina)
    rows = mycursor.fetchall()
    return rows

def ingresos_mysql(archivo_ingresos):
    # Borramos la vieja tabla de ingresos
    mycursor.execute('TRUNCATE ingresos')
    mydb.commit()

    # Subimos la nueva tabla de ingresos
    query = "LOAD DATA LOCAL INFILE '"
    query += archivo_ingresos
    query += "' INTO TABLE ingresos CHARACTER "
    query += "SET UTF8 FIELDS TERMINATED BY ',';"
    mycursor.execute(query)
    mydb.commit()

def fechas_fichaje_eaya(fecha_desde, fecha_hasta):
    sql_fichaje_eaya = "SELECT * FROM `fichaje` WHERE fecha BETWEEN "
    sql_fichaje_eaya += '"' + fecha_desde + '"' + ' and ' + '"' + fecha_hasta + '"' + ';'
    mycursor.execute(sql_fichaje_eaya)
    rows = mycursor.fetchall()
    return rows

def subir_fichaje(tabla, archivo):
    mycursor.execute("TRUNCATE " + tabla)
    mydb.commit()

    subir_fichaje_csv = "LOAD DATA LOCAL INFILE '" + archivo
    subir_fichaje_csv += "' INTO TABLE " + tabla + " CHARACTER SET UTF8 "
    subir_fichaje_csv += "FIELDS TERMINATED BY ',';"
    mycursor.execute(subir_fichaje_csv)
    mydb.commit()

def agenda_fichaje_eaya(fecha_desde, fecha_hasta):
    query = "SELECT agenda.Legajo, agenda.Nombre, agenda.Puesto,"
    query += " agenda.Sucursal, agenda.Provincia, ingresos.supervisor, "
    query += "ingresos.jefe_zonal, ingresos.jefe_reg, agenda.Fecha, "
    query += "agenda.HorarioEntrada, fichaje_eaya.ingreso, "
    query += "agenda.HorarioSalida, fichaje_eaya.salida FROM agenda LEFT JOIN "
    query += "fichaje_eaya ON agenda.Legajo = fichaje_eaya.legajo AND "
    query += "agenda.Fecha = fichaje_eaya.fecha LEFT JOIN ingresos ON "
    query += "agenda.Legajo = ingresos.legajo WHERE agenda.fecha BETWEEN '"
    query += fecha_desde + "' and " + "'" + fecha_hasta + "'" + ";"
    mycursor.execute(query)
    return mycursor.fetchall()

def subir_agenda(archivo_agenda):
    load_data_agenda = "LOAD DATA LOCAL INFILE '"
    load_data_agenda += archivo_agenda
    load_data_agenda += "' INTO TABLE agenda CHARACTER SET"
    load_data_agenda += " UTF8 FIELDS TERMINATED BY ',';"
    mycursor.execute(load_data_agenda)
    mydb.commit()
