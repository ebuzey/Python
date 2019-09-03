#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
