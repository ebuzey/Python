import random as ran


NUMERO_INFERIOR = 0
NUMERO_SUPERIOR = 100
JUGADAS = 100

# def cantidad_intentos_simple(posibilidades):
#     intentos = int(posibilidades * 0.1)
#     return intentos
#
# INTENTOS = cantidad_intentos_simple(NUMERO_SUPERIOR - NUMERO_INFERIOR)

# Pensar una cantidad de intentos de manera que el adivinar complejo gane entre un 50% o %60 y haya una diferenecia interesante con el adivinar simple
def cantidad_intentos_compleja(posibilidades):
    # rango = ran.uniform(0.05, 0.06)
    # intentos = round(posibilidades * rango)
    caluco_intentos = posibilidades
    contador = 0
    while caluco_intentos >= 1:
        caluco_intentos = caluco_intentos / 2
        contador += 1
    intentos = int(contador * 0.90)
    return intentos

INTENTOS = cantidad_intentos_compleja(NUMERO_SUPERIOR - NUMERO_INFERIOR)

def adivinar_numero_simple(numero_inferior, numero_superior):
    numero = ran.randint(numero_inferior, numero_superior)
    return numero

def adivinar_numero_comlejo(numero_inferior, numero_superior):
    numero = int((numero_inferior + numero_superior) / 2)
    return numero

def jugar(numero_inferior, numero_superior, intentos, estrategia):
    numero_magico = ran.randint(numero_inferior, numero_superior)
    for _ in range(intentos):
        numero_actual = estrategia(numero_inferior, numero_superior)
        if numero_actual < numero_magico:
            numero_inferior = numero_actual + 1
        elif numero_actual > numero_magico:
            numero_superior = numero_actual - 1
        else:
            return True
    return False

def repetir_jugada(jugadas, numero_inferior, numero_superior, intentos, estrategia):
    jugadas_ganadas = 0
    for _ in range(jugadas):
        resultado = jugar(numero_inferior, numero_superior, intentos, estrategia)
        if resultado:
            jugadas_ganadas += 1
    return jugadas_ganadas

if __name__ == '__main__':
    print(
        'La cantidad de jugadas complejas ganadas son: ',
         repetir_jugada(JUGADAS, NUMERO_INFERIOR, NUMERO_SUPERIOR, INTENTOS, adivinar_numero_comlejo)
         )

    print(
        'La cantidad de jugadas simples ganadas son: ',
         repetir_jugada(JUGADAS, NUMERO_INFERIOR, NUMERO_SUPERIOR, INTENTOS, adivinar_numero_simple)
         )
