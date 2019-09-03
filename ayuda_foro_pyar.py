#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def clasificador(numero):
    categorias = {
        1: 'Categoria Menor',
        4: 'Categoria Media Inferior',
        8: 'Categoria Media',
        14: 'Categoria Media Superior',
        25: 'Categoria Mayor'
        }
    for categoria, desc_cat in categorias.items():
        if numero >= categoria:
            resultado = desc_cat

    return resultado

if __name__ == '__main__':
    ejecutar = clasificador(12)
    print(ejecutar)
