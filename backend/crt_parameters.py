#-------------------------------------------------------------------------------------
# PARAMETROS FISICOS FIJOS DEL TUBO DE RAYOS CATODICOS (CRT)
# Este modulo contiene todas las constantes fisicas que no pueden ser modificadas por el usuario
# pero que son necesarias para los calculos del movimiento de electrones
#-------------------------------------------------------------------------------------

import math

#-------------------------------------------------------------------------------------
# CONSTANTES FISICAS UNIVERSALES
#-------------------------------------------------------------------------------------
# Carga del electron (negativa)
CARGA_ELECTRON = -1.602176634e-19  # Coulombs
# Masa del electron
MASA_ELECTRON = 9.1093837015e-31    # kg

#-------------------------------------------------------------------------------------
# DIMENSIONES DE LA PANTALLA DEL CRT
#-------------------------------------------------------------------------------------
# La pantalla es cuadrada como especifica el documento
TAMANO_PANTALLA = 0.20          # 20 cm de lado (orden de magnitud de decenas de cm)
ANCHO_PANTALLA = TAMANO_PANTALLA  # metros
ALTO_PANTALLA = TAMANO_PANTALLA # metros

# La pantalla tiene curvatura para permitir que los electrones golpeen cualquier punto
# Usaremos coordenadas planas pero con esta consideracion para los calculos
RADIO_CURVATURA_PANTALLA = 0.30  # Radio de curvatura en metros

#-------------------------------------------------------------------------------------
# DIMENSIONES Y POSICIONES DE LAS PLACAS DE DEFLEXION
#-------------------------------------------------------------------------------------
# Placas de deflexion vertical (controlan movimiento vertical del haz)
ANCHO_PLACAS_VERTICALES = 0.04    # 4 cm de ancho
ALTO_PLACAS_VERTICALES = 0.06   # 6 cm de alto
SEPARACION_PLACAS_VERTICALES = 0.015  # 1.5 cm de separacion entre placas

# Placas de deflexion horizontal (controlan movimiento horizontal del haz)
ANCHO_PLACAS_HORIZONTALES = 0.06   # 6 cm de ancho  
ALTO_PLACAS_HORIZONTALES = 0.04    # 4 cm de alto
SEPARACION_PLACAS_HORIZONTALES = 0.015  # 1.5 cm de separacion entre placas

#-------------------------------------------------------------------------------------
# DISTANCIAS DENTRO DEL TUBO CRT
#-------------------------------------------------------------------------------------
# Distancia desde el cañon de electrones hasta las placas verticales
DISTANCIA_CANON_A_PLACAS_VERTICALES = 0.05  # 5 cm

# Distancia desde las placas verticales hasta las placas horizontales
DISTANCIA_PLACAS_VERTICALES_A_HORIZONTALES = 0.03  # 3 cm

# Distancia desde las placas horizontales hasta la pantalla
DISTANCIA_PLACAS_HORIZONTALES_A_PANTALLA = 0.15  # 15 cm

# Distancia total desde el cañon hasta la pantalla
DISTANCIA_TOTAL_CANON_A_PANTALLA = (DISTANCIA_CANON_A_PLACAS_VERTICALES + 
                                   DISTANCIA_PLACAS_VERTICALES_A_HORIZONTALES + 
                                   DISTANCIA_PLACAS_HORIZONTALES_A_PANTALLA)

#-------------------------------------------------------------------------------------
# RANGOS DE VOLTAJES CONTROLABLES POR EL USUARIO
#-------------------------------------------------------------------------------------
# Rango de voltaje de aceleracion (voltios)
VOLTAJE_ACELERACION_MIN = 500     # Voltios minimos
VOLTAJE_ACELERACION_MAX = 5000    # Voltios maximos
VOLTAJE_ACELERACION_DEFAULT = 2000  # Voltaje por defecto

# Rango de voltaje para placas de deflexion vertical
VOLTAJE_VERTICAL_MIN = -200       # Voltios minimos (negativo para deflexion hacia abajo)
VOLTAJE_VERTICAL_MAX = 200        # Voltios maximos (positivo para deflexion hacia arriba)
VOLTAJE_VERTICAL_DEFAULT = 0      # Sin deflexion por defecto

# Rango de voltaje para placas de deflexion horizontal  
VOLTAJE_HORIZONTAL_MIN = -200     # Voltios minimos (negativo para deflexion hacia la izquierda)
VOLTAJE_HORIZONTAL_MAX = 200      # Voltios maximos (positivo para deflexion hacia la derecha)
VOLTAJE_HORIZONTAL_DEFAULT = 0    # Sin deflexion por defecto

#-------------------------------------------------------------------------------------
# PARAMETROS DE SIMULACION
#-------------------------------------------------------------------------------------
# Tiempo de persistencia en la pantalla (segundos)
TIEMPO_PERSISTENCIA_MIN = 0.1     # Minimo tiempo que permanece el punto
TIEMPO_PERSISTENCIA_MAX = 5.0     # Maximo tiempo que permanece el punto
TIEMPO_PERSISTENCIA_DEFAULT = 1.0 # Tiempo por defecto

# Resolucion temporal para calculos (segundos)
PASO_TIEMPO_CALCULO = 1e-9        # 1 nanosegundo para precision en los calculos

#-------------------------------------------------------------------------------------
# FUNCIONES AUXILIARES PARA VALIDACION DE PARAMETROS
#-------------------------------------------------------------------------------------
def validar_voltaje_aceleracion(voltaje):
    """Valida que el voltaje de aceleracion este dentro del rango permitido."""
    return VOLTAJE_ACELERACION_MIN <= voltaje <= VOLTAJE_ACELERACION_MAX

def validar_voltaje_vertical(voltaje):
    """Valida que el voltaje de deflexion vertical este dentro del rango permitido."""
    return VOLTAJE_VERTICAL_MIN <= voltaje <= VOLTAJE_VERTICAL_MAX

def validar_voltaje_horizontal(voltaje):
    """Valida que el voltaje de deflexion horizontal este dentro del rango permitido."""
    return VOLTAJE_HORIZONTAL_MIN <= voltaje <= VOLTAJE_HORIZONTAL_MAX

def validar_tiempo_persistencia(tiempo):
    """Valida que el tiempo de persistencia este dentro del rango permitido."""
    return TIEMPO_PERSISTENCIA_MIN <= tiempo <= TIEMPO_PERSISTENCIA_MAX

def obtener_parametros_sistema():
    """Devuelve un diccionario con todos los parametros del sistema para el frontend."""
    return {
        'pantalla': {
            'ancho': ANCHO_PANTALLA,
            'alto': ALTO_PANTALLA,
            'radio_curvatura': RADIO_CURVATURA_PANTALLA
        },
        'placas_verticales': {
            'ancho': ANCHO_PLACAS_VERTICALES,
            'alto': ALTO_PLACAS_VERTICALES,
            'separacion': SEPARACION_PLACAS_VERTICALES
        },
        'placas_horizontales': {
            'ancho': ANCHO_PLACAS_HORIZONTALES,
            'alto': ALTO_PLACAS_HORIZONTALES,
            'separacion': SEPARACION_PLACAS_HORIZONTALES
        },
        'distancias': {
            'canon_a_verticales': DISTANCIA_CANON_A_PLACAS_VERTICALES,
            'verticales_a_horizontales': DISTANCIA_PLACAS_VERTICALES_A_HORIZONTALES,
            'horizontales_a_pantalla': DISTANCIA_PLACAS_HORIZONTALES_A_PANTALLA,
            'total': DISTANCIA_TOTAL_CANON_A_PANTALLA
        },
        'rangos_voltaje': {
            'aceleracion': {
                'min': VOLTAJE_ACELERACION_MIN,
                'max': VOLTAJE_ACELERACION_MAX,
                'default': VOLTAJE_ACELERACION_DEFAULT
            },
            'vertical': {
                'min': VOLTAJE_VERTICAL_MIN,
                'max': VOLTAJE_VERTICAL_MAX,
                'default': VOLTAJE_VERTICAL_DEFAULT
            },
            'horizontal': {
                'min': VOLTAJE_HORIZONTAL_MIN,
                'max': VOLTAJE_HORIZONTAL_MAX,
                'default': VOLTAJE_HORIZONTAL_DEFAULT
            }
        },
        'simulacion': {
            'persistencia_min': TIEMPO_PERSISTENCIA_MIN,
            'persistencia_max': TIEMPO_PERSISTENCIA_MAX,
            'persistencia_default': TIEMPO_PERSISTENCIA_DEFAULT,
            'paso_tiempo': PASO_TIEMPO_CALCULO
        }
    }