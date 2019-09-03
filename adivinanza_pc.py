#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import random
# numero_magico = random.randint(0,100)

# from random import randint
# numero_magico = randint(0,100)

# import random as ran
#
# NUMERO_INFERIOR = 0
# NUMERO_SUPERIOR = 100
# INTENTOS = int(NUMERO_SUPERIOR * 0.1)
#
# numero_magico = ran.randint(NUMERO_INFERIOR, NUMERO_SUPERIOR + 1)
# numero_actual = NUMERO_INFERIOR - 1
# numero_inferior = NUMERO_INFERIOR
# numero_superior = NUMERO_SUPERIOR
#
#
# for _ in range(INTENTOS):
#     while numero_actual <= numero_inferior or numero_actual >= numero_superior:
#         numero_actual = input('Por favor, ingresa un número del ' + str(numero_inferior) + ' al ' + str(numero_superior) + ': ')
#         numero_actual = int(numero_actual)
#
#     if numero_actual < numero_magico:
#         print('El número es mayor')
#         numero_inferior = numero_actual
#     elif numero_actual > numero_magico:
#         print('El número es menor')
#         numero_superior = numero_actual
#     else:
#         print('\n***********\n* YOU WIN *\n***********\n')
#         break
#
# if numero_actual != numero_magico:
#     print('\n*************\n* GAME OVER *\n*************\n' + 'El número magico era: ' + str(numero_magico))

# CORREGIR TODO EL CODIGO, ES DECIR CONTEMPLAR LAS CONDICIONES POSIBLES Y PENSAR COMO HACER PARA QUE LA MAQUINA JUEGUE SOLA

import random as ran

NUMERO_INFERIOR = 0
NUMERO_SUPERIOR = 100
INTENTOS = int(NUMERO_SUPERIOR * 0.1)

numero_magico = ran.randint(NUMERO_INFERIOR, NUMERO_SUPERIOR + 1)
numero_actual = 0
numero_inferior = NUMERO_INFERIOR
numero_superior = NUMERO_SUPERIOR


for _ in range(INTENTOS):
    numero_actual = ran.randint(numero_inferior, numero_superior)
    print('Por favor, ingresa un número del ' + str(numero_inferior) + ' al ' + str(numero_superior) + ': ' + str(numero_actual))
    numero_actual = int(numero_actual)

    if numero_actual < numero_magico:
        print('El número es mayor')
        numero_inferior = numero_actual + 1
    elif numero_actual > numero_magico:
        print('El número es menor')
        numero_superior = numero_actual - 1
    else:
        print('\n***********\n* YOU WIN *\n***********\n')
        break

if numero_actual != numero_magico:
    print('\n*************\n* GAME OVER *\n*************\n' + 'El número magico era: ' + str(numero_magico))

# import random as ran
# import os
# import socket
#
# NUMERO_INFERIOR = 0
# NUMERO_SUPERIOR = 100
# INTENTOS = int(NUMERO_SUPERIOR * 0.1)
#
# numero_magico = ran.randint(NUMERO_INFERIOR, NUMERO_SUPERIOR + 1)
# numero_actual = NUMERO_INFERIOR - 1
# numero_inferior = NUMERO_INFERIOR
# numero_superior = NUMERO_SUPERIOR
# usuario = input('Por favor, ingresa tu nombre: ')
# pc = socket.gethostname()
# numero_pc = 0
#
# for _ in range(INTENTOS):
#     while numero_actual <= numero_inferior or numero_actual >= numero_superior:
#         numero_actual = input(usuario + ' por favor, ingresa un número del ' + str(numero_inferior) + ' al ' + str(numero_superior) + ': ')
#         numero_actual = int(numero_actual)
#
#     if numero_actual < numero_magico:
#         print('El número es mayor')
#         numero_inferior = numero_actual
#     elif numero_actual > numero_magico:
#         print('El número es menor')
#         numero_superior = numero_actual
#     else:
#         print('\n' + usuario + ' YOU WIN\n')
#         break
#
#     numero_pc = ran.randint(numero_inferior, numero_superior)
#     print(pc + ' por favor, ingresa un número del ' + str(numero_inferior) + ' al ' + str(numero_superior) + ': ' + str(numero_pc))
#     numero_pc = int(numero_pc)
#
#     if numero_pc < numero_magico:
#         print('El número es mayor')
#         numero_inferior = numero_pc
#     elif numero_pc > numero_magico:
#         print('El número es menor')
#         numero_superior = numero_pc
#     else:
#         print('\n' + pc + ' YOU WIN\n')
#         break
#
# if numero_actual != numero_magico:
#     print('\n*************\n* GAME OVER *\n*************\n' + 'El número magico era: ' + str(numero_magico))
# if numero_pc != numero_magico:
#     print('\n*************\n* GAME OVER *\n*************\n' + 'El número magico era: ' + str(numero_magico))
