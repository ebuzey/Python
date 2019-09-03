#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Actualmente se esta trabajando en la depuracion de este Código

import sys
from os import remove
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QDialog,
                             QFileDialog,
                             QMessageBox,
                             QAction,
                             QSplashScreen,
                             QProgressBar
                             )
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import *
import datetime as dt
from datetime import datetime, timedelta
import mysql.connector
import csv
import shutil
import time

'''
# Conexion mysql - ENTORNO DE DESARROLLO
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='entorno_desarrollo')
'''
# Conexion mysql
try:
    mydb = mysql.connector.connect(
        host='',
        user='',
        passwd='',
        database='')
except mysql.connector.errors.DatabaseError:
    app = QtWidgets.QApplication([])
    error_dialog = QtWidgets.QMessageBox()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("./imagenes/sistemas.png"),
                   QtGui.QIcon.Selected,
                   QtGui.QIcon.On)
    error_dialog.setWindowIcon(icon)
    error_dialog.about(error_dialog,
                       'Modulo Fichaje',
                       'Error de conexion, por favor verifique su enlace a '
                       'internet')
    app.exec_()
    sys.exit()


# Fecha para la generacion de nombres
fecha_nombre_archivos = dt.datetime.now()
fecha_nombre_archivos = fecha_nombre_archivos.strftime('%Y-%m-%d')
# Exportamos Agenda y generamos CSV
mycursor = mydb.cursor()
mycursor.execute('SELECT * FROM agenda')
rows = mycursor.fetchall()
archivo_salida = 'Resultado_Agenda ' + fecha_nombre_archivos + '.csv'
resultado_agenda = open(archivo_salida, 'w', encoding='utf8')
myFile = csv.writer(resultado_agenda)
myFile.writerows(rows)
resultado_agenda.close()
# Excepcion en caso de error al mover archivo
try:
    shutil.move(archivo_salida, './Descargas/Resultado_Agendas')
except shutil.Error:
    try:
        remove('./Descargas/Resultado_Agendas/' + archivo_salida)
        shutil.move(archivo_salida, './Descargas/Resultado_Agendas')
    except PermissionError:
        QMessageBox.about(
            error_dialog, "Modulo Fichaje",
            "Para continuar cierre el archivo " +
            archivo_salida + " e intentelo nuevamente")
        sys.exit()
mydb.commit()


class Principal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        QDialog.__init__(self)
        self.resize(800, 500)  # Tamaño inicial de la ventana 800x500
        # Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./imagenes/sistemas.png"),
                       QtGui.QIcon.Selected,
                       QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setWindowTitle("Modulo de Fichaje - Valor Humano v1.5")
        # Barra de estado
        self.statusBar().showMessage("Bienvenid@ - Departamento de Desarrollo "
                                     "y Nuevas Tecnologías - Gcia. Sistemas"
                                     " EAYA Consulting - 2019")
        # Objeto menuBar
        menu = self.menuBar()
        # Menú padre
        menu_actividad = menu.addMenu("&Actividad")
        # Menú padre
        menu_salir = menu.addMenu("&Salir")
        # Accion Menu Salir
        menu_salir.triggered.connect(self.menuSalir)
        # Agregar un elemento acción al menu_archivo
        menu_actividad_agenda = QAction(
                            QIcon('./imagenes/agenda.png'), "&Agenda", self)
        # Atajo de teclado
        menu_actividad_agenda.setShortcut("Ctrl+a")
        # Mensaje en la barra de estado
        menu_actividad_agenda.setStatusTip("Generar Agenda")
        # Lanzador
        menu_actividad_agenda.triggered.connect(self.menuActividadAgenda)
        # Agregar un elemento acción al menu_archivo
        menu_actividad_novedades = QAction(QIcon(
                    './imagenes/novedades.png'), '&Novedades', self)
        # Atajo de teclado
        menu_actividad_novedades.setShortcut("Ctrl+n")
        # Mensaje en la barra de estado
        menu_actividad_novedades.setStatusTip("Generar Novedades")
        menu_actividad_novedades.triggered.connect(self.menuActividadNovedades)
        menu_actividad_novedades_cierre = QAction(QIcon(
                    './imagenes/novedades.png'), '&Cierre Novedades', self)
        # Atajo de teclado
        menu_actividad_novedades_cierre.setShortcut("Ctrl+c")
        # Mensaje en la barra de estado
        menu_actividad_novedades_cierre.setStatusTip("Generar Cierre de Novedades")
        menu_actividad_novedades_cierre.triggered.connect(self.menuActividadCierreNovedades)

        menu_actividad.addAction(menu_actividad_agenda)
        menu_actividad.addAction(menu_actividad_novedades)
        menu_actividad.addAction(menu_actividad_novedades_cierre)


        menu_actividad.addAction(menu_actividad_agenda)
        menu_actividad.addAction(menu_actividad_novedades)

        # Vinculo la clase
        self.ventana_agenda = VentanaAgenda()
        self.ventana_novedades = VentanaNovedades()

        exitButton = QAction(QIcon('./imagenes/exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Salir del Modulo Fichaje')
        exitButton.triggered.connect(self.close)
        menu_salir.addAction(exitButton)

    def menuSalir(self):
        self.close()

    def menuActividadAgenda(self):
        self.ventana_agenda.exec_()

    def menuActividadNovedades(self):
        self.ventana_novedades.exec_()

    def menuActividadCierreNovedades(self):
        self.ventana_novedades.exec_()


class VentanaAgenda(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setFixedSize(574, 318)
        self.setWindowTitle("Generacion de Agenda")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./imagenes/sistemas.png"),
                       QtGui.QIcon.Selected,
                       QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("Bienvenid@ al modulo 'AGENDA'")
        self.label.setGeometry(QtCore.QRect(10, 10, 471, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color:#9370DB;")
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 60, 541, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.boton = QtWidgets.QPushButton(self.centralwidget)
        self.boton.setGeometry(QtCore.QRect(310, 250, 101, 31))
        self.boton.setText("Aceptar")
        self.boton.setEnabled(False)
        self.boton_cancelar = QtWidgets.QPushButton(self.centralwidget)
        self.boton_cancelar.setGeometry(QtCore.QRect(420, 250, 101, 31))
        self.boton_cancelar.setText("Cancelar")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 290, 521, 101))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 100, 355, 47))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 2)
        self.btn_seleccionar = QtWidgets.QPushButton(self.widget)
        self.btn_seleccionar.setObjectName("btn_seleccionar")
        self.gridLayout_2.addWidget(self.btn_seleccionar, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(20, 160, 495, 66))
        self.widget1.setObjectName("widget1")
        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.fecha_desde = QtWidgets.QDateEdit(self.widget1)
        self.fecha_desde.setDate(QtCore.QDate.currentDate().addDays(7))
        self.fecha_desde.setObjectName("fecha_desde")
        self.gridLayout.addWidget(self.fecha_desde, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.fecha_hasta = QtWidgets.QDateEdit(self.widget1)
        self.fecha_hasta.setDate(QtCore.QDate.currentDate().addDays(13))
        self.fecha_hasta.setObjectName("fecha_hasta")
        self.gridLayout.addWidget(self.fecha_hasta, 2, 1, 1, 1)
        self.label_6.setText("Seleccione el archivo: 'INGRESOS.CSV':")
        self.btn_seleccionar.setText("Seleccionar archivo")
        self.label_5.setText("<html><head/><body><p>Ningun archivo"
                             " seleccionado</p></body></html>")
        self.label_2.setText("A continuacion, seleccione las fechas con las"
                             "cuales se confeccionara 'AGENDA':")
        self.label_3.setText("Desde:")
        self.label_4.setText("Hasta:")

        # Conexion Funcion buscar_archivo
        #  self.buscar_archivo = buscar_archivo()
        self.btn_seleccionar.clicked.connect(self.buscar_archivo)
        # Conexion Funcion buscar_archivo
        # self.click = click()
        self.boton.clicked.connect(self.click)
        self.boton_cancelar.clicked.connect(self.click_cancelar)

    def click_cancelar(self):
        self.close()

    def buscar_archivo(self):
        global file
        global fecha_nombre_archivos
        file, _ = QFileDialog.getOpenFileName(self, 'Buscar Archivo')
        file_name = file.split('/')
        file_name = file_name[-1]

        while file_name != 'INGRESOS.csv' and file:
            QMessageBox.about(
                self,
                "Modulo Fichaje",
                "Archivo seleccionado INCORRECTO, por favor seleccione"
                " INGRESOS.csv")
            file, _ = QFileDialog.getOpenFileName(self, 'Buscar Archivo')
            file_name = file.split('/')
            file_name = file_name[-1]
            self.label_5.setText(file_name)
            self.boton.setEnabled(False)
        if file:
            self.label_5.setText(file_name)
            self.boton.setEnabled(True)
            return file

    def click(self):
        global fecha_nombre_archivos

        horarios_presta = open('Horarios Oficina y Contact.csv',
                               'r', encoding='utf-8')
        detalle_horarios_presta = horarios_presta.readlines()
        agenda_oficina = {}
        for linea in detalle_horarios_presta:
            valor = linea.split(';')
            legajo_ao = valor[0].strip()
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
            if legajo_ao not in agenda_oficina.keys():
                agenda_oficina[legajo_ao] = [ingreso_lunes, salida_lunes,
                                             ingreso_martes, salida_martes,
                                             ingreso_miercoles,
                                             salida_miercoles,
                                             ingreso_jueves, salida_jueves,
                                             ingreso_viernes, salida_viernes,
                                             ingreso_sabado, salida_sabado,
                                             ingreso_domingo, salida_domingo]
        inicio = self.fecha_desde.date()
        fin = self.fecha_hasta.date()
        total = inicio.daysTo(fin)
        lista_fechas = []
        contador = 0
        while contador <= total:
            lista_fechas.append(
                inicio.addDays(contador).toString('yyyy-MM-dd'))
            contador = contador + 1
        agenda = {}

        #
        # Genero 'agenda fecha.csv' y cargamos la informacion de ingresos,
        # pero previo a esto corrboramos que sea el archivo correcto
        #
        try:
            file_object = open(file, 'r', encoding='utf-8')
            encabezado = file_object.readline()
            cierre = file_object.readlines()
        except UnicodeDecodeError:
            QMessageBox.about(
                self,
                "Modulo Fichaje",
                "El formato del archivo 'INGRESOS.csv' es INCORRECTO.<br>"
                "<br>Por favor, abra el archivo con Excel y separe el texto "
                "en columnas.<br><p align = 'left'>Muchas gracias!</p>")
            sys.exit()
        encabezado_correcto = '\ufeffLEGAJO;APELLIDOS;NOMBRES;INGRESO;'
        encabezado_correcto += 'BAJA;USUARIA;DESC_TRAB;DESC_SUC;'
        encabezado_correcto += 'PROVINCIA;SUPERVISOR;JEFE_ZONAL;'
        encabezado_correcto += 'JEFE_REG\n'
        ingresos = {}
        # Verifico si el archivo ingresos es correcto:

        if encabezado != encabezado_correcto:
            QMessageBox.about(
                self,
                "Modulo Fichaje",
                "El formato del archivo 'INGRESOS.csv' es INCORRECTO.<br>"
                "<br>Por favor, pongase en contacto con el departamento de"
                " Desarrollo y Nuevas Tecnologias.<br><p align = 'center'>"
                "Muchas gracias!</p>")
            self.close()
        elif len(cierre) < 80:
            QMessageBox.about(
                self,
                "Modulo Fichaje",
                "La cantidad de registros del archivo 'INGRESOS.csv' es "
                "INCORRECTO.<br><br>Por favor, pongase en contacto con el "
                "departamento de Desarrollo y Nuevas "
                "Tecnologias.<br><p align = 'center'>Muchas gracias!</p>")
            self.close()
        else:
            for linea in cierre:
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
                if legajo not in agenda.keys() and len(baja) == 0:
                    agenda[legajo] = {
                            'nombre': apellido_nombre,
                            'puesto': puesto,
                            'sucursal': sucursal,
                            'provincia': provincia,
                            'supervisor': supervisor,
                            'zonal': zonal,
                            'regional': regional,
                            'lista_fechas': lista_fechas
                            }

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

            file_object.close()

            # Genero ingresos.csv

            archivo_ingresos = 'Ingresos ' + fecha_nombre_archivos + '.csv'
            file_ingresos = open(archivo_ingresos, 'w', encoding='utf-8')
            for legajo in ingresos:
                linea = legajo + ',' + ingresos[legajo]['nombre'] + ','
                linea += ingresos[legajo]['ingreso'] + ','
                linea += ingresos[legajo]['baja'] + ','
                linea += ingresos[legajo]['usuaria'] + ','
                linea += ingresos[legajo]['puesto'] + ','
                linea += ingresos[legajo]['sucursal'] + ','
                linea += ingresos[legajo]['provincia'] + ','
                linea += ingresos[legajo]['supervisor'] + ','
                linea += ingresos[legajo]['zonal'] + ','
                linea += ingresos[legajo]['regional'] + '\n'
                file_ingresos.write(linea)
            file_ingresos.close()
            try:
                archivo_agenda = 'Agenda ' + fecha_nombre_archivos + '.csv'
                file_object = open(archivo_agenda, 'w', encoding='utf-8')
                id = ''
                hora = 0
                for legajo, fecha in agenda.items():
                    for dia in range(0, len(agenda[legajo]['lista_fechas'])):
                        linea = id + ',' + legajo + ','
                        linea += agenda[legajo]['nombre'] + ','
                        linea += agenda[legajo]['puesto'] + ','
                        linea += agenda[legajo]['sucursal'] + ','
                        linea += agenda[legajo]['provincia'] + ','
                        linea += agenda[legajo]['supervisor'] + ','
                        linea += agenda[legajo]['zonal'] + ','
                        linea += agenda[legajo]['regional'] + ','
                        linea += str(agenda[legajo]['lista_fechas'][dia]) + ','
                        if legajo in agenda_oficina.keys():
                            linea += agenda_oficina[legajo][hora] + ','
                            hora += 1
                            linea += agenda_oficina[legajo][hora] + '\n'
                            hora += 1
                            if hora == 14:
                                hora = 0
                        else:
                            linea += '00:00' + ',' + '00:00' + '\n'
                        file_object.write(linea)
                QMessageBox.about(
                    self, "Modulo Fichaje", "La tabla " +
                    archivo_agenda + " se generó correctamente")
                file_object.close()

                fechas = 'SELECT agenda.`Fecha` FROM agenda group'
                fechas += ' by agenda.`Fecha`'
                consulta_fechas = mycursor.execute(fechas)
                consulta_fechas = mycursor.fetchall()
                dias_tabla = []
                for tupla in consulta_fechas:
                    for fecha in tupla:
                        if fecha is None:
                            continue
                        else:
                            dias_tabla.append(fecha.strftime("%Y-%m-%d"))
                comparacion = []
                for item in dias_tabla:
                    if item in lista_fechas:
                        comparacion.append(item)
                if len(comparacion) > 0:
                    QMessageBox.about(self,
                                      "Modulo Fichaje",
                                      "Operacion Cancelada<br><br>"
                                      "Los datos ingresados ya fueron "
                                      "cargados, verifique la "
                                      "información.<br>")
                    self.close()
                else:
                    load_data_agenda = "LOAD DATA LOCAL INFILE '"
                    load_data_agenda += archivo_agenda
                    load_data_agenda += "' INTO TABLE agenda CHARACTER SET"
                    load_data_agenda += " UTF8 FIELDS TERMINATED BY ',';"
                    mycursor.execute(load_data_agenda)
                    mydb.commit()

                    # Borramos la vieja tabla de ingresos
                    mycursor.execute('TRUNCATE ingresos')
                    mydb.commit()

                    # Subimos la nueva tabla de ingresos
                    load_data_ingresos = "LOAD DATA LOCAL INFILE '"
                    load_data_ingresos += archivo_ingresos
                    load_data_ingresos += "' INTO TABLE ingresos CHARACTER "
                    load_data_ingresos += "SET UTF8 FIELDS TERMINATED BY ',';"
                    mycursor.execute(load_data_ingresos)
                    mydb.commit()

                    # Elimino espacio en blanco de INGRESOS

                    correcion_ingresos = "UPDATE ingresos set jefe_reg = "
                    correcion_ingresos += "replace(jefe_reg, '\r','');"
                    mycursor.execute(correcion_ingresos)
                    mydb.commit()

                    QMessageBox.about(
                        self,
                        "Modulo Fichaje",
                        "La tabla INGRESOS se actualizo correctamente")
                    self.close()

            except shutil.Error:
                QMessageBox.about(
                    self, "Modulo Fichaje",
                    "No se pudo generar el reporte ya que el archivo " +
                    archivo_agenda + " se encuentra abierto.\n"
                    "Por favor, cierre el archivo e intentelo nuevamente")
            # Excepcion en caso de error al mover archivo
        try:
            shutil.move(archivo_ingresos, './Descargas/Ingresos')
        except shutil.Error:
            try:
                remove('./Descargas/Ingresos/' + archivo_ingresos)
                shutil.move(archivo_ingresos, './Descargas/Ingresos')
            except PermissionError:
                QMessageBox.about(
                    self, "Modulo Fichaje",
                    "Para continuar cierre el archivo " +
                    archivo_ingresos + " e intentelo nuevamente")
                sys.exit()
        try:
            shutil.move(archivo_agenda,
                        './Descargas/Generacion_Agendas')
        except shutil.Error:
            try:
                remove(
                    './Descargas/Generacion_Agendas/' +
                    archivo_agenda)
                shutil.move(archivo_agenda,
                            './Descargas/Generacion_Agendas')
            except PermissionError:
                QMessageBox.about(
                    self, "Modulo Fichaje",
                    "Para continuar cierre el archivo " +
                    archivo_agenda + " e intentelo nuevamente")
                sys.exit()


class VentanaNovedades(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setFixedSize(574, 318)
        self.setWindowTitle("Generacion de Novedades")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./imagenes/sistemas.png"),
                       QtGui.QIcon.Selected,
                       QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("Bienvenid@ al modulo 'NOVEDADES'")
        self.label.setGeometry(QtCore.QRect(10, 10, 471, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color:#9370DB;")
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 60, 541, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.boton = QtWidgets.QPushButton(self.centralwidget)
        self.boton.setGeometry(QtCore.QRect(310, 250, 101, 31))
        self.boton.setText("Aceptar")
        self.boton.setEnabled(False)
        self.boton_cancelar = QtWidgets.QPushButton(self.centralwidget)
        self.boton_cancelar.setGeometry(QtCore.QRect(420, 250, 101, 31))
        self.boton_cancelar.setText("Cancelar")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 290, 521, 101))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 100, 355, 47))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 2)
        self.btn_seleccionar = QtWidgets.QPushButton(self.widget)
        self.btn_seleccionar.setObjectName("btn_seleccionar")
        self.gridLayout_2.addWidget(self.btn_seleccionar, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 1, 1, 1)
        self.label_6.setText("Seleccione el archivo: 'NOVEDADES':")
        self.btn_seleccionar.setText("Seleccionar archivo")
        self.label_5.setText("<html><head/><body><p>Ningun archivo"
                             " seleccionado</p></body></html>")
        self.btn_seleccionar.clicked.connect(self.buscar_archivo)
        self.boton.clicked.connect(self.click_novedades)
        self.boton_cancelar.clicked.connect(self.click_cancelar)

    def click_cancelar(self):
        self.close()

    def buscar_archivo(self):
        global file_novedades
        file_novedades, _ = QFileDialog.getOpenFileName(self, 'Buscar Archivo')
        file_name = file_novedades.split('/')
        file_name = file_name[-1]
        if file_name != '':
            self.boton.setEnabled(True)
            self.label_5.setText(file_name)

        return file_novedades

    def click_novedades(self):
        global fecha_nombre_archivos
        # Transformo el fichaje de oficina en Diccionario
        try:
            file_object = open(file_novedades, 'r')
            encabezado = file_object.readline().strip()
            detalle_fichaje = file_object.readlines()
        except UnicodeDecodeError:
            QMessageBox.about(
                self,
                "Modulo Fichaje",
                "El formato del archivo selccionado no coincide con el de "
                "FICHAJE OFICINA.<br><br>Por favor, pongase en contacto con "
                "el departamento de Desarrollo y Nuevas Tecnologias.<br><p "
                "align = 'center'>Muchas gracias!</p>")
            sys.exit()

        encabezado_correcto = 'Usuario Nro.,Nombre,Fecha/Hora,Dispositivo Nro.'
        encabezado_correcto += ',Nombre del dispositivo,Tipo de registro,Descr'
        encabezado_correcto += 'ipción,Departamento,Posición,Código de tarea'
        if encabezado != encabezado_correcto:
            QMessageBox.about(
                self,
                "Modulo Fichaje",
                "Los registros del archivo selccionado no coincide con el de "
                "FICHAJE OFICINA.<br><br>Por favor, pongase en contacto con "
                "el departamento de Desarrollo y Nuevas Tecnologias.<br><p "
                "align = 'center'>Muchas gracias!</p>")
            sys.exit()

        fichaje_oficina = {}
        fechas_en_archivo = []
        for linea in detalle_fichaje:
            HorarioEntrada = dt.time(0, 0)
            HorarioSalida = dt.time(0, 0)
            valores = linea.split(',')
            legajo = valores[1]
            fecha_hora = valores[2].split()
            fecha = fecha_hora[0]
            if fecha not in fechas_en_archivo:
                fechas_en_archivo.append(fecha)
            hora = fecha_hora[1]
            hora = datetime.strptime(hora, '%H:%M:%S').time()
            descripcion = valores[4]
            if descripcion == 'Malaver E':
                HorarioEntrada = hora
            else:
                HorarioSalida = hora

            # Si no corresponde a un legajo, descarto el registro
            if legajo == 'Berna':
                continue
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
        # Genero el .csv con el detalle del fichaje oficina
        archivo_oficina = 'Fichaje_oficina ' + fecha_nombre_archivos + '.csv'
        file_archivo_oficina = open(archivo_oficina, 'w', encoding='utf8')
        for legajo, dictFechas in fichaje_oficina.items():
            for fecha, horarios in dictFechas.items():
                linea = legajo + ',' + fecha + ','
                linea += str(horarios[0]) + ',' + str(horarios[1]) + '\n'

                file_archivo_oficina.write(linea)
        file_archivo_oficina.close()

        # Borramos la tabla vieja de fichaje_oficina
        mycursor.execute('TRUNCATE fichaje_oficina')
        mydb.commit()
        # Subo fichaje_oficina a phpMyAdmin
        load_data_fichajeOficina = "LOAD DATA LOCAL INFILE '" + archivo_oficina
        load_data_fichajeOficina += "' INTO TABLE fichaje_oficina CHARACTER "
        load_data_fichajeOficina += "SET latin1 FIELDS TERMINATED BY ',';"
        mycursor.execute(load_data_fichajeOficina)
        mydb.commit()
        QMessageBox.about(
            self,
            "Modulo Fichaje",
            "La tabla oficina_fichaje se actualizo correctamente")
        self.close()
        # Excepcion en caso de error al mover archivo
        try:
            shutil.move(archivo_oficina,
                        './Descargas/Fichaje_Oficina')
        except shutil.Error:
            try:
                remove(
                    './Descargas/Fichaje_Oficina/' + archivo_oficina)
                shutil.move(archivo_oficina,
                            './Descargas/Fichaje_Oficina')
            except PermissionError:
                QMessageBox.about(
                    self, "Modulo Fichaje",
                    "Para continuar cierre el archivo " +
                    archivo_oficina + " e intentelo nuevamente")
                sys.exit()

        # Efectuo el cruce del fichaje_oficina y la AGENDA
        sql_oficina = 'SELECT agenda.Legajo, agenda.Nombre, '
        sql_oficina += 'agenda.Puesto, agenda.Supervisor, '
        sql_oficina += 'agenda.Zonal, agenda.Regional, '
        sql_oficina += 'agenda.Fecha, agenda.HorarioEntrada, '
        sql_oficina += 'ifnull(fichaje_oficina.horario_entrada, "00:00:00") AS'
        sql_oficina += ' Horario_Entrada_Fichaje, agenda.HorarioSalida, '
        sql_oficina += 'ifnull(fichaje_oficina.horario_salida, "00:00:00") AS '
        sql_oficina += 'Horario_Salida_Fichaje, agenda.Sucursal FROM agenda '
        sql_oficina += 'LEFT JOIN fichaje_oficina ON agenda.Legajo = '
        sql_oficina += 'fichaje_oficina.legajo AND agenda.Fecha = '
        sql_oficina += 'fichaje_oficina.fecha WHERE agenda.Fecha '
        sql_oficina += 'BETWEEN date_add(CURDATE(), INTERVAL -7 DAY) AND '
        sql_oficina += 'date_add(CURDATE(), INTERVAL -1 DAY);'

        consulta_sql_oficina = mycursor.execute(sql_oficina)
        consulta_sql_oficina = mycursor.fetchall()

        novedades_csv = {}
        fechas_en_query = []
        for tupla in consulta_sql_oficina:
            legajo = tupla[0].strip()
            puesto = tupla[2]
            supervisor = tupla[3]
            zonal = tupla[4]
            regional = tupla[5]
            sucursal = tupla[11]
            if ('OFICINA' not in sucursal or
                    sucursal == 'OFICINA OPERACIONES VENTAS'):
                continue
            if legajo is None:
                continue
            nombre = tupla[1]
            fecha = tupla[6]
            if fecha not in fechas_en_query:
                fechas_en_query.append(fecha)
            entrada_agenda = tupla[7]
            # Normalizacion formato hora
            if ':' in entrada_agenda:
                entrada_agenda = entrada_agenda.strip() + ':00'
                entrada_agenda = datetime.strptime(entrada_agenda.strip(),
                                                   '%H:%M:%S').time()
            entrada_fichaje = tupla[8]
            # Normalizacion formato hora
            if entrada_fichaje is not None and ':' in entrada_fichaje:
                entrada_fichaje = entrada_fichaje.replace(' ', '')
                entrada_fichaje = entrada_fichaje.replace('\r', '')
                entrada_fichaje = datetime.strptime(entrada_fichaje.strip(),
                                                    '%H:%M:%S').time()
            elif entrada_fichaje is not None and '\r' in entrada_fichaje:
                entrada_fichaje = entrada_fichaje.replace('\r', '00:00:00')
                entrada_fichaje = datetime.strptime(entrada_fichaje.strip(),
                                                    '%H:%M:%S').time()
            elif entrada_fichaje is None:
                entrada_fichaje = '00:00:00'
                entrada_fichaje = datetime.strptime(entrada_fichaje.strip(),
                                                    '%H:%M:%S').time()
            estado_entrada = ''

            salida_agenda = tupla[9].strip().replace('\n', '')
            # Normalizacion formato hora
            if ':' in salida_agenda:
                salida_agenda = salida_agenda.strip() + ':00'
                salida_agenda = datetime.strptime(salida_agenda.strip(),
                                                  '%H:%M:%S').time()
            salida_fichaje = tupla[10]
            # Normalizacion formato hora
            if salida_fichaje is not None and ':' in salida_fichaje:
                salida_fichaje = salida_fichaje.replace('\r', '')
                salida_fichaje = salida_fichaje.replace(' ', '')
                salida_fichaje = datetime.strptime(salida_fichaje.strip(),
                                                   '%H:%M:%S').time()
            elif salida_fichaje is not None and '\r' in salida_fichaje:
                salida_fichaje = salida_fichaje.replace('\r', '00:00:00')
                salida_fichaje = datetime.strptime(salida_fichaje.strip(),
                                                   '%H:%M:%S').time()
            elif salida_fichaje is None:
                salida_fichaje = '00:00:00'
                salida_fichaje = datetime.strptime(salida_fichaje.strip(),
                                                   '%H:%M:%S').time()
            estado_salida = ''

            opciones_agenda = [
                'Accion Móvil', 'Visitador', 'Vendedor Telefonica', 'ART',
                'Capacitación', 'Citación Judicial', 'Donación de sangre',
                'Elecciones', 'Estudio', 'Examen', 'Excedencia',
                'Ausencia por Feriado', 'Franco ganado', 'Franco',
                'Licencia deportiva', 'Maternidad', 'Matrimonio',
                'Matrimonio de hijo', 'Mudanza', 'Nacimiento', 'Paro general',
                'Reserva de puesto', 'Sin goce de sueldo', 'Suspensión',
                'Tramite prematrimonial', 'Vacaciones', 'Enfermedad', 'Gremial',
                'Vacaciones Adicionales Jefes', 'Dia de Cumpleaños',
                'Home Office', 'Baja Despido', 'Baja Renuncia', 'Baja Abandono',
                'Trabajo fuera de oficina'
                ]

            # Comienzo a corroborar los tipos de ausentismos
            # Campos Ingreso
            # 1 - Horarios Agenda
            if (isinstance(entrada_agenda, dt.time)
                    and isinstance(entrada_fichaje, dt.time)):
                if entrada_agenda == dt.time(0, 0):
                    estado_entrada = 'INCONSISTENCIA: No completo la agenda.'
                    if (entrada_fichaje is None
                            or entrada_fichaje == dt.time(0, 0)):
                        estado_entrada = 'INCONSISTENCIA: No completo la '
                        estado_entrada += 'agenda y no hay registros de '
                        estado_entrada += 'fichaje.'
                elif entrada_fichaje == dt.time(0, 0):
                    estado_entrada = 'No se registro fichaje'
                elif entrada_fichaje <= (dt.datetime.combine(dt.date(1, 1, 1), entrada_agenda) + dt.timedelta(minutes=3)).time():
                    # estado_entrada = 'Correcto'
                    continue
                else:
                    estado_entrada = 'INCONSISTENCIA: Ingreso tarde'
            # 2 - El resto de las opciones
            elif entrada_agenda in opciones_agenda:
                if (entrada_fichaje == '' or entrada_fichaje is None
                        or entrada_fichaje == dt.time(0, 0, 0)):
                    estado_entrada = 'Correcto'
                else:
                    estado_entrada = 'INCONSISTENCIA: Se informo: '
                    estado_entrada += entrada_agenda + ' y se registro fichaje'
                    estado_entrada += ' de ingreso'
            elif (entrada_agenda is not None
                    and entrada_agenda == dt.time(0, 0)):
                estado_entrada = 'INCONSISTENCIA: No completo la agenda.'
                if entrada_agenda is None:
                    estado_entrada = 'INCONSISTENCIA: No completo la agenda y'
                    estado_entrada += ' no hay registros de fichaje.'
                    entrada_agenda = '00:00:00'
            elif entrada_fichaje is None:
                estado_entrada = 'No hay registros'
            elif entrada_agenda is None:
                estado_entrada = 'INCONSISTENCIA: No completo la agenda.'

            # Campos Salida
            # 1 - Horarios Agenda
            if (isinstance(salida_agenda, dt.time)
                    and isinstance(salida_fichaje, dt.time)):
                if salida_agenda == dt.time(0, 0):
                    estado_salida = 'INCONSISTENCIA: No completo la agenda.'
                    if (salida_fichaje is None
                            or salida_fichaje == dt.time(0, 0)):
                        estado_salida = 'INCONSISTENCIA: No completo la agenda'
                        estado_salida += ' y no hay registros de fichaje.'
                elif salida_fichaje == dt.time(0, 0):
                    estado_salida = 'No se registro fichaje'
                elif salida_fichaje >= salida_agenda:
                    estado_salida = 'Correcto'
                else:
                    estado_salida = 'INCONSISTENCIA: Se retiro antes'
                salida_fichaje = str(salida_fichaje)
                salida_agenda = str(salida_agenda)
                FMT = '%H:%M:%S'
                tdelta = (datetime.strptime(salida_fichaje, FMT) -
                          datetime.strptime(salida_agenda, FMT))
                if (estado_entrada == 'Correcto' and estado_salida
                        == 'Correcto' and tdelta >= dt.timedelta(minutes=30)):
                    estado_salida = 'Atencion: Horas Extras > '
                    estado_salida += str(tdelta) + ' Hs.'

            # 2 - El resto de las opciones
            elif salida_agenda in opciones_agenda:
                if (salida_fichaje == '' or salida_fichaje is None
                        or salida_fichaje == dt.time(0, 0, 0)):
                    estado_salida = 'Correcto'
                else:
                    estado_salida = 'INCONSISTENCIA: Se informo: '
                    estado_salida += salida_agenda + ' y se registro fichaje'
                    estado_salida += ' de ingreso'
            elif salida_agenda is not None and salida_agenda == dt.time(0, 0):
                estado_salida = 'INCONSISTENCIA: No completo la agenda.'
                if salida_fichaje is None:
                    estado_salida = 'INCONSISTENCIA: No completo la agenda y '
                    estado_salida += 'no hay registros de fichaje.'
            elif salida_fichaje is None:
                estado_salida = 'No hay registros de fichaje'
            elif salida_agenda is None:
                estado_salida = 'INCONSISTENCIA: No completo la agenda.'

            if legajo not in novedades_csv.keys():
                novedades_csv[legajo] = {
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
            elif fecha not in novedades_csv[legajo]['agenda']:
                novedades_csv[legajo]['agenda'].append({
                        'fecha': fecha,
                        'entrada_agenda': entrada_agenda,
                        'entrada_fichaje': entrada_fichaje,
                        'entrada_estado': estado_entrada,
                        'salida_agenda': salida_agenda,
                        'salida_fichaje': salida_fichaje,
                        'salida_estado': estado_salida
                    })
        archivo_novedades_oficina = 'Novedades_Oficina '
        archivo_novedades_oficina += fecha_nombre_archivos + '.csv'
        file_object = open(archivo_novedades_oficina, 'w', encoding='utf8')
        id = ''
        for clave, valor in novedades_csv.items():
            legajo = clave
            datos = valor['datos']
            fechas = valor['agenda']
            for fecha in fechas:
                # pegar conversion de fechas
                fecha['fecha'] = fecha['fecha'].strftime('%Y-%m-%d')
                if isinstance(fecha['entrada_agenda'], dt.time):
                    fecha['entrada_agenda'] = "{:%H:%M:%S}".format(fecha['entrada_agenda'])
                if isinstance(fecha['entrada_fichaje'], dt.time):
                    fecha['entrada_fichaje'] = "{:%H:%M:%S}".format(fecha['entrada_fichaje'])
                if isinstance(fecha['entrada_agenda'], dt.time):
                    fecha['entrada_agenda'] = "{:%H:%M:%S}".format(fecha['entrada_agenda'])
                if isinstance(fecha['salida_agenda'], dt.time):
                    fecha['salida_agenda'] = "{:%H:%M:%S}".format(fecha['salida_agenda'])
                if isinstance(fecha['salida_fichaje'], dt.time):
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

        # Previo a subir el archivo de novedades, debemos constatar que las
        # fechas_en_archivo no esten tabla novedades_oficina
        file_object.close()
        sql_fechas_tbl_nov = "SELECT fecha FROM `novedades_oficina` GROUP BY "
        sql_fechas_tbl_nov += "fecha;"
        consulta_fechas = mycursor.execute(sql_fechas_tbl_nov)
        consulta_fechas = mycursor.fetchall()
        dias_tbl_nov = []
        for tupla in consulta_fechas:
            for fecha in tupla:
                if fecha is None:
                    continue
                else:
                    dias_tbl_nov.append(fecha.strftime("%Y-%m-%d"))
        comparacion = []
        fechas_repetida = []
        for item in dias_tbl_nov:
            if item in fechas_en_query:
                comparacion.append(item)
        if len(comparacion) > 0:
            for fecha in comparacion:
                fechas_repetida.append(fecha)
            fechas_repetida = ', '.join(fechas_repetida)
            QMessageBox.about(self,
                              "Modulo Fichaje",
                              "Operacion Cancelada<br><br>"
                              "Las fechas " + fechas_repetida + " ya fueron "
                              "cargadas, exporte nuevamente el fichaje de "
                              "oficina.<br>")
            self.close()
        else:
            load_data_novedades_oficina = "LOAD DATA LOCAL INFILE '"
            load_data_novedades_oficina += archivo_novedades_oficina
            load_data_novedades_oficina += "' INTO TABLE novedades_oficina "
            load_data_novedades_oficina += "CHARACTER SET utf8 FIELDS "
            load_data_novedades_oficina += "TERMINATED BY ',';"
            mycursor.execute(load_data_novedades_oficina)
            mydb.commit()
            QMessageBox.about(
                self,
                "Modulo Fichaje",
                "Las novedades se actualizaron correctamente")
            self.close()
            try:
                shutil.move(archivo_novedades_oficina,
                            './Descargas/Novedades_Oficina')
            except shutil.Error:
                try:
                    remove('./Descargas/Novedades_Oficina/' +
                           archivo_novedades_oficina)
                    shutil.move(archivo_novedades_oficina,
                                './Descargas/Novedades_Oficina')
                except PermissionError:
                    QMessageBox.about(
                        self, "Modulo Fichaje",
                        "Para continuar cierre el archivo " +
                        archivo_novedades_oficina + " e intentelo nuevamente")
                    sys.exit()
        # NOTE: 1 Normalizacion de fichaje, determinar que normallizamos para
        # no hacerlo con la tabla entera,2 Query que unifica Agenda con
        # fichaje_oficina 3 Calculo las novedades.
        # Normalizacion del formato de fichaje:
        '''
        sql_fichaje_eaya = "SELECT * FROM `fichaje` WHERE MONTH(fecha)="
        sql_fichaje_eaya += "MONTH(CURDATE()) AND YEAR(fecha)=YEAR(CURDATE());"
        '''
        sql_fichaje_eaya = "SELECT * FROM `fichaje` WHERE fecha BETWEEN "
        sql_fichaje_eaya += "date_add(CURDATE(), INTERVAL -7 DAY) AND "
        sql_fichaje_eaya += "date_add(CURDATE(), INTERVAL -1 DAY);"
        sql_fichaje = mycursor.execute(sql_fichaje_eaya)
        sql_fichaje = mycursor.fetchall()
        fichaje_csv = {}
        id = ''
        for tupla in sql_fichaje:
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
            if legajo not in fichaje_csv.keys():
                fichaje_csv[legajo] = {fecha: [ingreso, salida]}
            # Si el legajo esta y tambien la fecha, verifico y modifico la hora
            elif fecha in fichaje_csv[legajo].keys():
                dictFechas = fichaje_csv[legajo]
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
                dictFechas = fichaje_csv[legajo]
                dictFechas[fecha] = [ingreso, salida]
        # Genero un csv con dicha informacion:
        archivo_fichaje_eaya = 'Fichaje_eaya ' + fecha_nombre_archivos + '.csv'
        file_archivo_fichaje_eaya = open(archivo_fichaje_eaya, 'w',
                                         encoding='utf8')
        for legajo, dictFechas in fichaje_csv.items():
            for fecha, horarios in dictFechas.items():
                linea = id + ',' + legajo + ',' + fecha.strftime("%Y-%m-%d")
                linea += ',' + str(horarios[0]) + ',' + str(horarios[1]) + '\n'
                file_archivo_fichaje_eaya.write(linea)

        file_archivo_fichaje_eaya.close()
        borrar_fichaje_eaya = "TRUNCATE fichaje_eaya"
        mycursor.execute(borrar_fichaje_eaya)
        mydb.commit()
        # Subo el csv
        subir_fichaje_csv = "LOAD DATA LOCAL INFILE '" + archivo_fichaje_eaya
        subir_fichaje_csv += "' INTO TABLE fichaje_eaya CHARACTER SET UTF8 "
        subir_fichaje_csv += "FIELDS TERMINATED BY ',';"
        mycursor.execute(subir_fichaje_csv)
        mydb.commit()
        try:
            shutil.move(archivo_fichaje_eaya,
                        './Descargas/Fichaje_Eaya')
        except shutil.Error:
            try:
                remove('./Descargas/Fichaje_Eaya/' +
                       archivo_fichaje_eaya)
                shutil.move(archivo_fichaje_eaya,
                            './Descargas/Fichaje_Eaya')
            except PermissionError:
                QMessageBox.about(
                    self, "Modulo Fichaje",
                    "Para continuar cierre el archivo " +
                    archivo_fichaje_eaya + " e intentelo nuevamente")
                sys.exit()

        # Unir tabla agenda con Fichaje_eaya
        sql_agenda_fichaje = "SELECT agenda.Legajo, agenda.Nombre, "
        sql_agenda_fichaje += "agenda.Puesto, agenda.Sucursal, "
        sql_agenda_fichaje += "agenda.Provincia, agenda.Supervisor, "
        sql_agenda_fichaje += "agenda.Zonal, agenda.Regional, agenda.Fecha, "
        sql_agenda_fichaje += "agenda.HorarioEntrada, fichaje_eaya.ingreso, "
        sql_agenda_fichaje += "agenda.HorarioSalida, fichaje_eaya.salida "
        sql_agenda_fichaje += "FROM agenda LEFT JOIN fichaje_eaya ON "
        sql_agenda_fichaje += "agenda.Legajo = fichaje_eaya.legajo AND "
        sql_agenda_fichaje += "agenda.Fecha = fichaje_eaya.fecha WHERE "
        sql_agenda_fichaje += "agenda.fecha BETWEEN date_add(CURDATE(), "
        sql_agenda_fichaje += "INTERVAL -7 DAY) AND date_add(CURDATE(), "
        sql_agenda_fichaje += "INTERVAL -1 DAY);"
        sql_agenda_fichaje = mycursor.execute(sql_agenda_fichaje)
        sql_agenda_fichaje = mycursor.fetchall()
        novedades_eaya = {}
        fechas_en_query = []
        for tupla in sql_agenda_fichaje:
            nombre = tupla[1]
            legajo = tupla[0]
            puesto = tupla[2]
            sucursal = tupla[3]
            supervisor = tupla[5]
            zonal = tupla[6]
            regional = tupla[7]
            if 'OFICINA' in sucursal:
                continue
            if legajo is None:
                continue
            fecha = tupla[8]

            if fecha not in fechas_en_query:
                fechas_en_query.append(fecha)
            entrada_agenda = tupla[9]
            if ':' in entrada_agenda:
                entrada_agenda = entrada_agenda.strip() + ':00'
                entrada_agenda = datetime.strptime(entrada_agenda.strip(),
                                                   '%H:%M:%S').time()
            elif entrada_agenda is None:
                entrada_agenda = dt.time(0, 0)
            entrada_fichaje = tupla[10]
            if entrada_fichaje is None:
                entrada_fichaje = dt.time(0, 0)
            else:
                entrada_fichaje = (dt.datetime.min + entrada_fichaje).time()
            estado_entrada = ''
            salida_agenda = tupla[11].strip().replace('\n', '')
            if ':' in salida_agenda:
                salida_agenda = salida_agenda.strip() + ':00'
                salida_agenda = datetime.strptime(salida_agenda.strip(),
                                                  '%H:%M:%S').time()
            elif salida_agenda is None:
                salida_agenda = dt.time(0, 0)
            salida_fichaje = tupla[12]
            if salida_fichaje is None:
                salida_fichaje = dt.time(0, 0)
            else:
                salida_fichaje = (dt.datetime.min + salida_fichaje).time()
            estado_salida = ''

            opciones_agenda = [
                'Accion Móvil', 'Visitador', 'Vendedor Telefonica', 'ART',
                'Capacitación', 'Citación Judicial', 'Donación de sangre',
                'Elecciones', 'Estudio', 'Examen', 'Excedencia',
                'Ausencia por Feriado', 'Franco ganado', 'Franco',
                'Licencia deportiva', 'Maternidad', 'Matrimonio',
                'Matrimonio de hijo', 'Mudanza', 'Nacimiento', 'Paro general',
                'Reserva de puesto', 'Sin goce de sueldo', 'Suspensión',
                'Tramite prematrimonial', 'Vacaciones', 'Enfermedad', 'Gremial',
                'Vacaciones Adicionales Jefes', 'Dia de Cumpleaños',
                'Home Office', 'Baja Despido', 'Baja Renuncia', 'Baja Abandono',
                'Trabajo fuera de oficina'
                ]

            # Comienzo a corroborar los tipos de ausentismos
            # Campos Ingreso
            # 1 - Horarios Agenda
            if (isinstance(entrada_agenda, dt.time)
                    and isinstance(entrada_fichaje, dt.time)):
                if entrada_agenda == dt.time(0, 0):
                    estado_entrada = 'INCONSISTENCIA: No completo la agenda.'
                    if (entrada_fichaje is None
                            or entrada_fichaje == dt.time(0, 0)):
                        estado_entrada = 'INCONSISTENCIA: No completo la '
                        estado_entrada += 'agenda y no hay registros de '
                        estado_entrada += 'fichaje.'
                elif entrada_fichaje == dt.time(0, 0):
                    estado_entrada = 'No se registro fichaje'
                elif entrada_fichaje <= (dt.datetime.combine(dt.date(1, 1, 1), entrada_agenda) + dt.timedelta(minutes=3)).time():
                    estado_entrada = 'Correcto'
                else:
                    estado_entrada = 'INCONSISTENCIA: Ingreso tarde'
            # 2 - El resto de las opciones
            elif entrada_agenda in opciones_agenda:
                if (entrada_fichaje == '' or entrada_fichaje is None
                        or entrada_fichaje == dt.time(0, 0)):
                    estado_entrada = 'Correcto'
                else:
                    estado_entrada = 'INCONSISTENCIA: Se informo: '
                    estado_entrada += entrada_agenda + ' y se registro fichaje'
                    estado_entrada += ' de ingreso'
            elif (entrada_agenda is not None
                    and entrada_agenda == dt.time(0, 0)):
                estado_entrada = 'INCONSISTENCIA: No completo la agenda.'
                if entrada_agenda is None:
                    estado_entrada = 'INCONSISTENCIA: No completo la agenda y'
                    estado_entrada += ' no hay registros de fichaje.'
                    entrada_agenda = dt.time(0, 0)
            elif entrada_fichaje is None:
                estado_entrada = 'No hay registros'
            elif entrada_agenda is None:
                estado_entrada = 'INCONSISTENCIA: No completo la agenda.'

            # Campos Salida
            # 1 - Horarios Agenda
            if (isinstance(salida_agenda, dt.time)
                    and isinstance(salida_fichaje, dt.time)):
                if salida_agenda == dt.time(0, 0):
                    estado_salida = 'INCONSISTENCIA: No completo la agenda.'
                    if (salida_fichaje is None
                            or salida_fichaje == dt.time(0, 0)):
                        estado_salida = 'INCONSISTENCIA: No completo la agenda'
                        estado_salida += ' y no hay registros de fichaje.'
                elif salida_fichaje == dt.time(0, 0):
                    estado_salida = 'No se registro fichaje'
                elif salida_fichaje >= salida_agenda:
                    estado_salida = 'Correcto'
                else:
                    estado_salida = 'INCONSISTENCIA: Se retiro antes'
                salida_fichaje = str(salida_fichaje)
                salida_agenda = str(salida_agenda)
                FMT = '%H:%M:%S'
                tdelta = (datetime.strptime(salida_fichaje, FMT) -
                          datetime.strptime(salida_agenda, FMT))
                if (estado_entrada == 'Correcto' and estado_salida
                        == 'Correcto' and tdelta >= dt.timedelta(minutes=30)):
                    estado_salida = 'Atencion: Horas Extras > '
                    estado_salida += str(tdelta) + ' Hs.'

            # 2 - El resto de las opciones
            elif salida_agenda in opciones_agenda:
                if (salida_fichaje == '' or salida_fichaje is None
                        or salida_fichaje == dt.time(0, 0)):
                    estado_salida = 'Correcto'
                else:
                    estado_salida = 'INCONSISTENCIA: Se informo: '
                    estado_salida += salida_agenda + ' y se registro fichaje'
                    estado_salida += ' de ingreso'
            elif salida_agenda is not None and salida_agenda == dt.time(0, 0):
                estado_salida = 'INCONSISTENCIA: No completo la agenda.'
                if salida_fichaje is None:
                    estado_salida = 'INCONSISTENCIA: No completo la agenda y '
                    estado_salida += 'no hay registros de fichaje.'
            elif salida_fichaje is None:
                estado_salida = 'No hay registros de fichaje'
            elif salida_agenda is None:
                estado_salida = 'INCONSISTENCIA: No completo la agenda.'
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
        archivo_novedades_eaya = 'Novedades_Eaya '
        archivo_novedades_eaya += fecha_nombre_archivos + '.csv'
        file_object = open(archivo_novedades_eaya, 'w', encoding='utf8')
        id = ''
        for clave, valor in novedades_eaya.items():
            legajo = clave
            datos = valor['datos']
            fechas = valor['agenda']
            for fecha in fechas:
                if isinstance(fecha['fecha'], dt.date):
                    fecha['fecha'] = fecha['fecha'].strftime('%Y-%m-%d')
                if isinstance(fecha['entrada_agenda'], dt.time):
                    fecha['entrada_agenda'] = "{:%H:%M:%S}".format(fecha['entrada_agenda'])
                if isinstance(fecha['entrada_fichaje'], dt.time):
                    fecha['entrada_fichaje'] = "{:%H:%M:%S}".format(fecha['entrada_fichaje'])
                if isinstance(fecha['entrada_agenda'], dt.time):
                    fecha['entrada_agenda'] = "{:%H:%M:%S}".format(fecha['entrada_agenda'])
                if isinstance(fecha['salida_agenda'], dt.time):
                    fecha['salida_agenda'] = "{:%H:%M:%S}".format(fecha['salida_agenda'])
                if isinstance(fecha['salida_fichaje'], dt.time):
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
        # Previo a subir el archivo de novedades, debemos constatar que las
        # fechas_en_archivo no esten tabla novedades_oficina

        file_object.close()
        sql_fechas_tbl_nov = "SELECT fecha FROM `novedades_eaya` GROUP BY "
        sql_fechas_tbl_nov += "fecha;"
        consulta_fechas = mycursor.execute(sql_fechas_tbl_nov)
        consulta_fechas = mycursor.fetchall()
        dias_tbl_nov = []
        for tupla in consulta_fechas:
            for fecha in tupla:
                if fecha is None or fecha == '':
                    continue
                else:
                    if isinstance(fecha, dt.date):
                        fecha = fecha.strftime('%Y-%m-%d')
                    dias_tbl_nov.append(fecha)
        comparacion = []
        fechas_repetida = []
        for item in dias_tbl_nov:
            if item in fechas_en_query:
                comparacion.append(item)
        if len(comparacion) > 0:
            for fecha in comparacion:
                if isinstance(fecha, dt.date):
                    fecha = fecha.strftime('%Y-%m-%d')
                fechas_repetida.append(fecha)
            fechas_repetida = ','.join(fechas_repetida)
            fechas_repetida.strftime('%Y-%m-%d')
            # TODO: Error que me arroja, listas no posee el atributo strftime, quizas con un str en linea 1428 funciona
            QMessageBox.about(self,
                              "Modulo Fichaje",
                              "Operacion Cancelada<br><br>"
                              "Las fechas " + fechas_repetida + " ya fueron "
                              "cargadas, exporte nuevamente el fichaje de "
                              "oficina.<br>")
            self.close()
        else:
            load_data_novedades_eaya = "LOAD DATA LOCAL INFILE '"
            load_data_novedades_eaya += archivo_novedades_eaya
            load_data_novedades_eaya += "' INTO TABLE novedades_eaya "
            load_data_novedades_eaya += "CHARACTER SET utf8 FIELDS "
            load_data_novedades_eaya += "TERMINATED BY ',';"
            mycursor.execute(load_data_novedades_eaya)
            mydb.commit()
            QMessageBox.about(
                self,
                "Modulo Fichaje",
                "Las novedades de Ventas se actualizaron correctamente")
            self.close()

            try:
                shutil.move(archivo_novedades_eaya,
                            './Descargas/Novedades_Eaya')
            except shutil.Error:
                try:
                    remove('./Descargas/Novedades_Eaya/' +
                           archivo_novedades_eaya)
                    shutil.move(archivo_novedades_eaya,
                                './Descargas/Novedades_Eaya')
                except PermissionError:
                    QMessageBox.about(
                        self, "Modulo Fichaje",
                        "Para continuar cierre el archivo " +
                        archivo_novedades_eaya + " e intentelo nuevamente")
                    sys.exit()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap('./imagenes/sistemas.png')

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setEnabled(False)

    progressBar = QProgressBar(splash)
    progressBar.setMaximum(10)
    progressBar.setGeometry(195, 180, 10, 10)
    progressBar.resize(180, 10)

    splash.show()

    for i in range(1, 11):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    principal = Principal()
    principal.show()
    splash.finish(principal)
    sys.exit(app.exec_())
