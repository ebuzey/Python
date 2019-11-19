#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fichaje

def test_fecha_inicio_novedades():
    try:
        fichaje.fecha_inicio_novedades('agenda')
    except ValueError:
        # Ok esperamos ValueError ya que agenda no es una tabla valida
        pass

    fecha = fichaje.fecha_inicio_novedades('novedades_eaya')

    assert fecha != None, 'fecha_inicio_novedades en la tabla novedades_eaya.'

    assert isinstance(fecha, str), 'fecha_inicio_novedades no retorna un str.'

def test_fecha_fin_novedades():

    fecha = fichaje.fecha_fin_novedades()
    assert isinstance(fecha, str), 'fecha_fin_novedades no retorna un str.'

    fecha = datetime.strptime(fecha, '%Y-%m-%d')
    assert fecha + datedelta(day=1) != now.datetime(), 'fecha_fin_novedades no retorna hoy - 1.'

    

if __name__ == '__main__':
    test_fecha_inicio_novedades()
