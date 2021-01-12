#!/usr/bin/env python3
import RPi.GPIO as GPIO  # importa GPIO
from hx711 import HX711  # importa la clase HX711
GPIO.setwarnings(False)  # elimina los warnings

try:
    GPIO.setmode(GPIO.BCM)  # Pines GPIO en numeración BCM
    # Crea un objeto hx que represente el chip HX711 real
    # Los parámetros de entrada obligatorios son solo 'Pin_Dato' y 'PD_sck'
    hx = HX711(dout_pin=21, pd_sck_pin=20)
    # Medir la tara y guardar el valor como compensación para el canal actual
    # y ganancia seleccionada. Eso significa canal A y ganancia 128
    err = hx.zero()
    # Verifica si todo está correcto
    if err:
        raise ValueError('La tara no se puede definir.')

    reading = hx.get_raw_data_mean()
    if reading:     # Verificar si el valor correcto 
                    # ahora el valor está cerca de 0
        print('Datos restados por compensación pero todavía no convertidos a unidades:',
              reading)
    else:
        print('Dato invalido', reading)

    # Para calcular la tasa de conversión a algunas unidades, en en este caso gramos,
    # Se debe partir de un peso conocido para ajustar.
    input('Coloque un peso conocido en la balanza y luego presione Enter')
    reading = hx.get_data_mean()
    if reading:
        print('Valor medio de HX711 restado para compensar:', reading)
        known_weight_grams = input(
            'Escriba cuántos gramos eran y presiona Enter: ')
        try:
            value = float(known_weight_grams)
            print(value, 'gramos')
        except ValueError:
            print('Entero o flotante esperado y tengo:',
                  known_weight_grams)

       
        # establecer la relación de escala para un canal en particular y una ganancia
        # utilizada para calcular la conversión a unidades. El argumento requerido es solo
        # una relación de escala. Sin argumentos 'canal' y 'ganancia_A' establece
        # la relación entre el canal actual y la ganancia.
        ratio = reading / value   # calcular la relación para el canal A y la ganancia 128
        hx.set_scale_ratio(ratio) # Determina la proporción para el canal actual
        print('Relación de peso establecida.')
    else:
        raise ValueError('No se puede calcular el valor medio . ERROR', reading)

    # Leer datos varias veces y devolver el valor medio
    # restado por compensación y escalado a las 
    # unidades deseadas. En este caso en gramos.
    print("Ahora, leeré datos en un bucle infinito. Para salir presione 'CTRL + C'")
    input('Presione Enter para comenzar a leer')
    #print('El peso actual en la balanza en gramos es: ')
    while True:
        print("El peso actual en gramos es de %.2f" % (hx.get_weight_mean(20)))

except (KeyboardInterrupt, SystemExit):
    print('Chau :)')

finally:
    GPIO.cleanup()
