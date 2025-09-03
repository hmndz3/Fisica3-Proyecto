#-------------------------------------------------------------------------------------
# GENERADOR DE SEÑALES SINUSOIDALES PARA FIGURAS DE LISSAJOUS
# Este modulo se encarga de generar las señales de voltaje sinusoidales que se aplican
# a las placas de deflexion para crear las famosas Figuras de Lissajous
#-------------------------------------------------------------------------------------

import math
import numpy as np
import crt_parameters

#-------------------------------------------------------------------------------------
# PARAMETROS DE LAS SEÑALES SINUSOIDALES
#-------------------------------------------------------------------------------------
# Rangos de frecuencia para las señales sinusoidales (Hz)
FRECUENCIA_MIN = 0.1       # 0.1 Hz minimo
FRECUENCIA_MAX = 10.0      # 10 Hz maximo
FRECUENCIA_DEFAULT = 1.0   # 1 Hz por defecto

# Rangos de fase para las señales sinusoidales (radianes)
FASE_MIN = 0.0             # 0 radianes (0 grados)
FASE_MAX = 2 * math.pi     # 2π radianes (360 grados)
FASE_DEFAULT = 0.0         # Sin desfase por defecto

# Amplitud de las señales (usara los rangos de voltaje definidos en parametros)
AMPLITUD_VERTICAL_DEFAULT = 100    # 100V de amplitud para deflexion vertical
AMPLITUD_HORIZONTAL_DEFAULT = 100  # 100V de amplitud para deflexion horizontal

#-------------------------------------------------------------------------------------
# FUNCIONES DE VALIDACION PARA PARAMETROS DE LISSAJOUS
#-------------------------------------------------------------------------------------
def validar_frecuencia(frecuencia):
    """Valida que la frecuencia este dentro del rango permitido."""
    return FRECUENCIA_MIN <= frecuencia <= FRECUENCIA_MAX

def validar_fase(fase):
    """Valida que la fase este dentro del rango permitido."""
    return FASE_MIN <= fase <= FASE_MAX

def validar_amplitud_vertical(amplitud):
    """Valida que la amplitud vertical no exceda los rangos de voltaje."""
    return amplitud <= min(abs(crt_parameters.VOLTAJE_VERTICAL_MIN), abs(crt_parameters.VOLTAJE_VERTICAL_MAX))

def validar_amplitud_horizontal(amplitud):
    """Valida que la amplitud horizontal no exceda los rangos de voltaje."""
    return amplitud <= min(abs(crt_parameters.VOLTAJE_HORIZONTAL_MIN), abs(crt_parameters.VOLTAJE_HORIZONTAL_MAX))

#-------------------------------------------------------------------------------------
# FUNCIONES GENERADORAS DE SEÑALES SINUSOIDALES
#-------------------------------------------------------------------------------------
def generar_senal_vertical(tiempo, frecuencia_vertical, fase_vertical, amplitud_vertical):
    """
    Genera el voltaje sinusoidal para las placas de deflexion vertical.
    V_vertical(t) = A * sin(2π * f * t + φ)
    """
    if not validar_frecuencia(frecuencia_vertical):
        raise ValueError(f"Frecuencia vertical fuera de rango: {frecuencia_vertical}")
    
    if not validar_fase(fase_vertical):
        raise ValueError(f"Fase vertical fuera de rango: {fase_vertical}")
        
    if not validar_amplitud_vertical(amplitud_vertical):
        raise ValueError(f"Amplitud vertical fuera de rango: {amplitud_vertical}")
    
    # Calcular voltaje sinusoidal
    voltaje_vertical = amplitud_vertical * math.sin(2 * math.pi * frecuencia_vertical * tiempo + fase_vertical)
    
    # Asegurar que este dentro de los limites de voltaje
    voltaje_vertical = max(crt_parameters.VOLTAJE_VERTICAL_MIN, min(crt_parameters.VOLTAJE_VERTICAL_MAX, voltaje_vertical))
    
    return voltaje_vertical

def generar_senal_horizontal(tiempo, frecuencia_horizontal, fase_horizontal, amplitud_horizontal):
    """
    Genera el voltaje sinusoidal para las placas de deflexion horizontal.
    V_horizontal(t) = A * sin(2π * f * t + φ)
    """
    if not validar_frecuencia(frecuencia_horizontal):
        raise ValueError(f"Frecuencia horizontal fuera de rango: {frecuencia_horizontal}")
    
    if not validar_fase(fase_horizontal):
        raise ValueError(f"Fase horizontal fuera de rango: {fase_horizontal}")
        
    if not validar_amplitud_horizontal(amplitud_horizontal):
        raise ValueError(f"Amplitud horizontal fuera de rango: {amplitud_horizontal}")
    
    # Calcular voltaje sinusoidal
    voltaje_horizontal = amplitud_horizontal * math.sin(2 * math.pi * frecuencia_horizontal * tiempo + fase_horizontal)
    
    # Asegurar que este dentro de los limites de voltaje
    voltaje_horizontal = max(crt_parameters.VOLTAJE_HORIZONTAL_MIN, min(crt_parameters.VOLTAJE_HORIZONTAL_MAX, voltaje_horizontal))
    
    return voltaje_horizontal

#-------------------------------------------------------------------------------------
# FUNCIONES PARA GENERAR FIGURAS DE LISSAJOUS ESPECIFICAS
#-------------------------------------------------------------------------------------
def generar_voltajes_lissajous(tiempo, config_lissajous):
    """
    Genera ambos voltajes simultaneamente para crear una Figura de Lissajous.
    config_lissajous debe contener:
    - frecuencia_vertical, fase_vertical, amplitud_vertical
    - frecuencia_horizontal, fase_horizontal, amplitud_horizontal
    """
    try:
        voltaje_vertical = generar_senal_vertical(
            tiempo,
            config_lissajous['frecuencia_vertical'],
            config_lissajous['fase_vertical'],
            config_lissajous['amplitud_vertical']
        )
        
        voltaje_horizontal = generar_senal_horizontal(
            tiempo,
            config_lissajous['frecuencia_horizontal'],
            config_lissajous['fase_horizontal'],
            config_lissajous['amplitud_horizontal']
        )
        
        return {
            'voltaje_vertical': voltaje_vertical,
            'voltaje_horizontal': voltaje_horizontal,
            'tiempo': tiempo
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'voltaje_vertical': 0,
            'voltaje_horizontal': 0
        }

#-------------------------------------------------------------------------------------
# PRESETS DE FIGURAS DE LISSAJOUS CLASICAS
#-------------------------------------------------------------------------------------
def obtener_presets_lissajous():
    """
    Devuelve configuraciones predefinidas para generar Figuras de Lissajous clasicas.
    Estas son las figuras mas comunes que se ven en osciloscopios.
    """
    presets = {
        'circulo': {
            'nombre': 'Círculo',
            'descripcion': 'Frecuencias iguales, fase de 90°',
            'frecuencia_vertical': 1.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 100,
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': math.pi / 2,  # 90 grados
            'amplitud_horizontal': 100
        },
        'linea_diagonal': {
            'nombre': 'Línea Diagonal',
            'descripcion': 'Frecuencias iguales, sin desfase',
            'frecuencia_vertical': 1.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 100,
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': 0.0,
            'amplitud_horizontal': 100
        },
        'elipse': {
            'nombre': 'Elipse',
            'descripcion': 'Frecuencias iguales, fase de 45°',
            'frecuencia_vertical': 1.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 100,
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': math.pi / 4,  # 45 grados
            'amplitud_horizontal': 100
        },
        'ocho': {
            'nombre': 'Figura en 8',
            'descripcion': 'Relación de frecuencia 2:1',
            'frecuencia_vertical': 2.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 100,
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': 0.0,
            'amplitud_horizontal': 100
        },
        'trebol': {
            'nombre': 'Trébol',
            'descripcion': 'Relación de frecuencia 3:1',
            'frecuencia_vertical': 3.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 100,
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': 0.0,
            'amplitud_horizontal': 100
        },
        'mariposa': {
            'nombre': 'Mariposa',
            'descripcion': 'Relación de frecuencia 3:2 con desfase',
            'frecuencia_vertical': 3.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 100,
            'frecuencia_horizontal': 2.0,
            'fase_horizontal': math.pi / 6,  # 30 grados
            'amplitud_horizontal': 100
        }
    }
    
    return presets

#-------------------------------------------------------------------------------------
# FUNCIONES PARA ANIMACION TEMPORAL DE LISSAJOUS
#-------------------------------------------------------------------------------------
def generar_secuencia_lissajous(config_lissajous, duracion_segundos, fps=30):
    """
    Genera una secuencia temporal de voltajes para animar una Figura de Lissajous.
    duracion_segundos: cuanto tiempo dura la animacion
    fps: frames per second para la animacion
    """
    num_frames = int(duracion_segundos * fps)
    secuencia = []
    
    for frame in range(num_frames):
        tiempo_actual = frame / fps
        
        voltajes = generar_voltajes_lissajous(tiempo_actual, config_lissajous)
        
        # Agregar informacion del frame para la animacion
        voltajes['frame'] = frame
        voltajes['tiempo_total'] = duracion_segundos
        voltajes['fps'] = fps
        
        secuencia.append(voltajes)
    
    return secuencia

def calcular_periodo_lissajous(frecuencia_vertical, frecuencia_horizontal):
    """
    Calcula el periodo de repeticion de una Figura de Lissajous.
    El periodo es el minimo comun multiplo de los periodos individuales.
    """
    # Periodos individuales
    periodo_vertical = 1.0 / frecuencia_vertical
    periodo_horizontal = 1.0 / frecuencia_horizontal
    
    # Para simplificar, usamos el maximo de los dos periodos multiplicado por un factor
    # En la practica, el calculo del MCM requiere trabajar con fracciones
    periodo_lissajous = max(periodo_vertical, periodo_horizontal) * 10
    
    return periodo_lissajous

#-------------------------------------------------------------------------------------
# FUNCIONES DE CONTROL EN TIEMPO REAL
#-------------------------------------------------------------------------------------
def actualizar_parametros_lissajous(config_actual, nuevos_parametros):
    """
    Actualiza los parametros de Lissajous de manera segura, validando cada valor.
    """
    config_actualizada = config_actual.copy()
    
    # Validar y actualizar frecuencia vertical
    if 'frecuencia_vertical' in nuevos_parametros:
        if validar_frecuencia(nuevos_parametros['frecuencia_vertical']):
            config_actualizada['frecuencia_vertical'] = nuevos_parametros['frecuencia_vertical']
    
    # Validar y actualizar fase vertical
    if 'fase_vertical' in nuevos_parametros:
        if validar_fase(nuevos_parametros['fase_vertical']):
            config_actualizada['fase_vertical'] = nuevos_parametros['fase_vertical']
    
    # Validar y actualizar amplitud vertical
    if 'amplitud_vertical' in nuevos_parametros:
        if validar_amplitud_vertical(nuevos_parametros['amplitud_vertical']):
            config_actualizada['amplitud_vertical'] = nuevos_parametros['amplitud_vertical']
    
    # Validar y actualizar frecuencia horizontal
    if 'frecuencia_horizontal' in nuevos_parametros:
        if validar_frecuencia(nuevos_parametros['frecuencia_horizontal']):
            config_actualizada['frecuencia_horizontal'] = nuevos_parametros['frecuencia_horizontal']
    
    # Validar y actualizar fase horizontal
    if 'fase_horizontal' in nuevos_parametros:
        if validar_fase(nuevos_parametros['fase_horizontal']):
            config_actualizada['fase_horizontal'] = nuevos_parametros['fase_horizontal']
    
    # Validar y actualizar amplitud horizontal
    if 'amplitud_horizontal' in nuevos_parametros:
        if validar_amplitud_horizontal(nuevos_parametros['amplitud_horizontal']):
            config_actualizada['amplitud_horizontal'] = nuevos_parametros['amplitud_horizontal']
    
    return config_actualizada

def obtener_configuracion_default_lissajous():
    """
    Devuelve una configuracion por defecto para las Figuras de Lissajous.
    """
    return {
        'frecuencia_vertical': FRECUENCIA_DEFAULT,
        'fase_vertical': FASE_DEFAULT,
        'amplitud_vertical': AMPLITUD_VERTICAL_DEFAULT,
        'frecuencia_horizontal': FRECUENCIA_DEFAULT,
        'fase_horizontal': FASE_DEFAULT,
        'amplitud_horizontal': AMPLITUD_HORIZONTAL_DEFAULT
    }

#-------------------------------------------------------------------------------------
# FUNCIONES AUXILIARES PARA EL FRONTEND
#-------------------------------------------------------------------------------------
def obtener_info_lissajous():
    """
    Devuelve informacion completa sobre los parametros de Lissajous para el frontend.
    """
    return {
        'rangos': {
            'frecuencia': {
                'min': FRECUENCIA_MIN,
                'max': FRECUENCIA_MAX,
                'default': FRECUENCIA_DEFAULT,
                'unidad': 'Hz'
            },
            'fase': {
                'min': FASE_MIN,
                'max': FASE_MAX,
                'default': FASE_DEFAULT,
                'unidad': 'radianes',
                'max_grados': 360
            },
            'amplitud_vertical': {
                'min': 0,
                'max': min(abs(crt_parameters.VOLTAJE_VERTICAL_MIN), abs(crt_parameters.VOLTAJE_VERTICAL_MAX)),
                'default': AMPLITUD_VERTICAL_DEFAULT,
                'unidad': 'V'
            },
            'amplitud_horizontal': {
                'min': 0,
                'max': min(abs(crt_parameters.VOLTAJE_HORIZONTAL_MIN), abs(crt_parameters.VOLTAJE_HORIZONTAL_MAX)),
                'default': AMPLITUD_HORIZONTAL_DEFAULT,
                'unidad': 'V'
            }
        },
        'presets': obtener_presets_lissajous(),
        'configuracion_default': obtener_configuracion_default_lissajous()
    }

def convertir_grados_a_radianes(grados):
    """Convierte grados a radianes para uso interno."""
    return grados * math.pi / 180

def convertir_radianes_a_grados(radianes):
    """Convierte radianes a grados para mostrar al usuario."""
    return radianes * 180 / math.pi