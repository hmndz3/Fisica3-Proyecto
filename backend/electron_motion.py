#-------------------------------------------------------------------------------------
# CALCULOS DE MOVIMIENTO DE ELECTRONES EN EL CRT
# Este modulo contiene todas las funciones para calcular la trayectoria de los electrones
# desde el cañon hasta la pantalla, considerando los efectos de las placas de deflexion
#-------------------------------------------------------------------------------------

import math
import numpy as np
from crt_parameters import *

#-------------------------------------------------------------------------------------
# FUNCIONES DE VELOCIDAD INICIAL Y ACELERACION
#-------------------------------------------------------------------------------------
def calcular_velocidad_inicial(voltaje_aceleracion):
    """
    Calcula la velocidad inicial del electron despues de ser acelerado por el voltaje.
    Usa la ecuacion de energia cinetica: (1/2)mv^2 = eV
    Por lo tanto: v = sqrt(2eV/m)
    """
    if not validar_voltaje_aceleracion(voltaje_aceleracion):
        raise ValueError(f"Voltaje de aceleracion fuera de rango: {voltaje_aceleracion}")
    
    # Energia cinetica ganada por el electron
    energia_cinetica = abs(CARGA_ELECTRON) * voltaje_aceleracion
    
    # Velocidad inicial en direccion horizontal (hacia la pantalla)
    velocidad_inicial = math.sqrt(2 * energia_cinetica / MASA_ELECTRON)
    
    return velocidad_inicial

#-------------------------------------------------------------------------------------
# FUNCIONES DE CAMPO ELECTRICO Y FUERZA
#-------------------------------------------------------------------------------------
def calcular_campo_electrico_vertical(voltaje_vertical):
    """
    Calcula la intensidad del campo electrico entre las placas verticales.
    Campo uniforme: E = V/d donde d es la separacion entre placas
    """
    if not validar_voltaje_vertical(voltaje_vertical):
        raise ValueError(f"Voltaje vertical fuera de rango: {voltaje_vertical}")
    
    # Campo electrico vertical (positivo hacia arriba)
    campo_electrico = voltaje_vertical / SEPARACION_PLACAS_VERTICALES
    return campo_electrico

def calcular_campo_electrico_horizontal(voltaje_horizontal):
    """
    Calcula la intensidad del campo electrico entre las placas horizontales.
    Campo uniforme: E = V/d donde d es la separacion entre placas
    """
    if not validar_voltaje_horizontal(voltaje_horizontal):
        raise ValueError(f"Voltaje horizontal fuera de rango: {voltaje_horizontal}")
    
    # Campo electrico horizontal (positivo hacia la derecha)
    campo_electrico = voltaje_horizontal / SEPARACION_PLACAS_HORIZONTALES
    return campo_electrico

def calcular_aceleracion(campo_electrico):
    """
    Calcula la aceleracion del electron en un campo electrico.
    F = qE y F = ma, por lo tanto a = qE/m
    """
    aceleracion = (CARGA_ELECTRON * campo_electrico) / MASA_ELECTRON
    return aceleracion

#-------------------------------------------------------------------------------------
# FUNCIONES DE TRAYECTORIA DEL ELECTRON
#-------------------------------------------------------------------------------------
def calcular_movimiento_en_placas_verticales(velocidad_inicial, voltaje_vertical):
    """
    Calcula el movimiento del electron mientras pasa por las placas de deflexion vertical.
    Movimiento uniformemente acelerado en direccion vertical.
    """
    # Tiempo que el electron pasa entre las placas verticales
    tiempo_en_placas = ANCHO_PLACAS_VERTICALES / velocidad_inicial
    
    # Campo electrico y aceleracion vertical
    campo_vertical = calcular_campo_electrico_vertical(voltaje_vertical)
    aceleracion_vertical = calcular_aceleracion(campo_vertical)
    
    # Posicion vertical al salir de las placas: y = (1/2)at^2
    deflexion_vertical = 0.5 * aceleracion_vertical * (tiempo_en_placas ** 2)
    
    # Velocidad vertical al salir de las placas: v = at
    velocidad_vertical = aceleracion_vertical * tiempo_en_placas
    
    return {
        'deflexion': deflexion_vertical,
        'velocidad_vertical': velocidad_vertical,
        'tiempo_en_placas': tiempo_en_placas
    }

def calcular_movimiento_en_placas_horizontales(velocidad_inicial, velocidad_vertical, voltaje_horizontal):
    """
    Calcula el movimiento del electron mientras pasa por las placas de deflexion horizontal.
    El electron ya tiene velocidad vertical de las placas anteriores.
    """
    # Tiempo que el electron pasa entre las placas horizontales
    tiempo_en_placas = ANCHO_PLACAS_HORIZONTALES / velocidad_inicial
    
    # Campo electrico y aceleracion horizontal
    campo_horizontal = calcular_campo_electrico_horizontal(voltaje_horizontal)
    aceleracion_horizontal = calcular_aceleracion(campo_horizontal)
    
    # Deflexion horizontal adicional: x = (1/2)at^2
    deflexion_horizontal = 0.5 * aceleracion_horizontal * (tiempo_en_placas ** 2)
    
    # Deflexion vertical adicional por movimiento previo: y = v*t + (1/2)at^2
    deflexion_vertical_adicional = velocidad_vertical * tiempo_en_placas
    
    # Velocidad horizontal al salir de las placas
    velocidad_horizontal = aceleracion_horizontal * tiempo_en_placas
    
    return {
        'deflexion_horizontal': deflexion_horizontal,
        'deflexion_vertical_adicional': deflexion_vertical_adicional,
        'velocidad_horizontal': velocidad_horizontal,
        'tiempo_en_placas': tiempo_en_placas
    }

def calcular_movimiento_libre_hasta_pantalla(velocidad_inicial, velocidad_vertical, velocidad_horizontal):
    """
    Calcula el movimiento del electron desde las placas horizontales hasta la pantalla.
    Movimiento rectilineo uniforme (no hay mas campos electricos).
    """
    # Tiempo de vuelo libre hasta la pantalla
    tiempo_vuelo_libre = DISTANCIA_PLACAS_HORIZONTALES_A_PANTALLA / velocidad_inicial
    
    # Deflexion adicional durante el vuelo libre
    deflexion_vertical_libre = velocidad_vertical * tiempo_vuelo_libre
    deflexion_horizontal_libre = velocidad_horizontal * tiempo_vuelo_libre
    
    return {
        'deflexion_vertical_libre': deflexion_vertical_libre,
        'deflexion_horizontal_libre': deflexion_horizontal_libre,
        'tiempo_vuelo_libre': tiempo_vuelo_libre
    }

#-------------------------------------------------------------------------------------
# FUNCION PRINCIPAL PARA CALCULAR POSICION FINAL
#-------------------------------------------------------------------------------------
def calcular_posicion_final_electron(voltaje_aceleracion, voltaje_vertical, voltaje_horizontal):
    """
    Calcula la posicion final donde el electron impacta la pantalla.
    Esta es la funcion principal que combina todos los calculos anteriores.
    """
    try:
        # Paso 1: Calcular velocidad inicial por aceleracion
        velocidad_inicial = calcular_velocidad_inicial(voltaje_aceleracion)
        
        # Paso 2: Movimiento en placas verticales
        resultado_vertical = calcular_movimiento_en_placas_verticales(velocidad_inicial, voltaje_vertical)
        deflexion_y_placas_verticales = resultado_vertical['deflexion']
        velocidad_vertical = resultado_vertical['velocidad_vertical']
        
        # Paso 3: Movimiento entre placas verticales y horizontales (vuelo libre)
        tiempo_entre_placas = DISTANCIA_PLACAS_VERTICALES_A_HORIZONTALES / velocidad_inicial
        deflexion_y_entre_placas = velocidad_vertical * tiempo_entre_placas
        
        # Paso 4: Movimiento en placas horizontales
        resultado_horizontal = calcular_movimiento_en_placas_horizontales(
            velocidad_inicial, velocidad_vertical, voltaje_horizontal)
        deflexion_x_placas_horizontales = resultado_horizontal['deflexion_horizontal']
        deflexion_y_placas_horizontales = resultado_horizontal['deflexion_vertical_adicional']
        velocidad_horizontal = resultado_horizontal['velocidad_horizontal']
        
        # Paso 5: Vuelo libre hasta la pantalla
        resultado_libre = calcular_movimiento_libre_hasta_pantalla(
            velocidad_inicial, velocidad_vertical, velocidad_horizontal)
        deflexion_x_libre = resultado_libre['deflexion_horizontal_libre']
        deflexion_y_libre = resultado_libre['deflexion_vertical_libre']
        
        # Paso 6: Posicion final en la pantalla
        # El centro de la pantalla es (0, 0)
        posicion_x_final = (deflexion_x_placas_horizontales + deflexion_x_libre)
        posicion_y_final = (deflexion_y_placas_verticales + deflexion_y_entre_placas + 
                           deflexion_y_placas_horizontales + deflexion_y_libre)
        
        # Verificar si el electron impacta dentro de la pantalla
        dentro_pantalla_x = abs(posicion_x_final) <= ANCHO_PANTALLA / 2
        dentro_pantalla_y = abs(posicion_y_final) <= ALTO_PANTALLA / 2
        dentro_pantalla = dentro_pantalla_x and dentro_pantalla_y
        
        return {
            'posicion_x': posicion_x_final,
            'posicion_y': posicion_y_final,
            'dentro_pantalla': dentro_pantalla,
            'velocidad_inicial': velocidad_inicial,
            'velocidad_final_x': velocidad_horizontal,
            'velocidad_final_y': velocidad_vertical,
            'tiempo_total': (resultado_vertical['tiempo_en_placas'] + tiempo_entre_placas + 
                           resultado_horizontal['tiempo_en_placas'] + resultado_libre['tiempo_vuelo_libre'])
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'posicion_x': 0,
            'posicion_y': 0,
            'dentro_pantalla': False
        }

#-------------------------------------------------------------------------------------
# FUNCIONES PARA OBTENER TRAYECTORIA COMPLETA
#-------------------------------------------------------------------------------------
def generar_trayectoria_completa(voltaje_aceleracion, voltaje_vertical, voltaje_horizontal, num_puntos=100):
    """
    Genera la trayectoria completa del electron con puntos intermedios para animacion.
    Devuelve una lista de posiciones (x, y, z) a lo largo del tiempo.
    """
    trayectoria = []
    
    try:
        velocidad_inicial = calcular_velocidad_inicial(voltaje_aceleracion)
        
        # Generar puntos en cada seccion del CRT
        # Seccion 1: Desde el cañon hasta las placas verticales
        for i in range(num_puntos // 4):
            t = i * (DISTANCIA_CANON_A_PLACAS_VERTICALES / velocidad_inicial) / (num_puntos // 4)
            x = velocidad_inicial * t
            y = 0
            z = 0
            trayectoria.append({'x': x, 'y': y, 'z': z, 'seccion': 'canon_a_verticales'})
        
        # Aqui se pueden agregar mas secciones para una animacion mas detallada
        # Por ahora retornamos solo la posicion final para probar
        resultado_final = calcular_posicion_final_electron(voltaje_aceleracion, voltaje_vertical, voltaje_horizontal)
        
        trayectoria.append({
            'x': DISTANCIA_TOTAL_CANON_A_PANTALLA,
            'y': resultado_final['posicion_y'],
            'z': resultado_final['posicion_x'],
            'seccion': 'pantalla'
        })
        
        return trayectoria
        
    except Exception as e:
        return [{'error': str(e)}]