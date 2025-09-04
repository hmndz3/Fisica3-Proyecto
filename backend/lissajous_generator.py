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
# FUNCIONES GENERADORAS DE SEÑALES SINUSOIDALES CORREGIDAS
#-------------------------------------------------------------------------------------
def generar_senal_vertical(tiempo, frecuencia_vertical, fase_vertical, amplitud_vertical):
    """
    Genera el voltaje sinusoidal para las placas de deflexion vertical.
    V_vertical(t) = A * sin(2π * f * t + φ)
    
    CORREGIDO: fase_vertical se espera en RADIANES
    """
    if not validar_frecuencia(frecuencia_vertical):
        raise ValueError(f"Frecuencia vertical fuera de rango: {frecuencia_vertical}")
    
    if not validar_amplitud_vertical(amplitud_vertical):
        raise ValueError(f"Amplitud vertical fuera de rango: {amplitud_vertical}")
    
    # IMPORTANTE: tiempo debe empezar desde 0 para figuras correctas
    # Calcular voltaje sinusoidal - fase ya en radianes
    voltaje_vertical = amplitud_vertical * math.sin(
        2 * math.pi * frecuencia_vertical * tiempo + fase_vertical
    )
    
    # Asegurar que este dentro de los limites de voltaje
    voltaje_vertical = max(
        crt_parameters.VOLTAJE_VERTICAL_MIN, 
        min(crt_parameters.VOLTAJE_VERTICAL_MAX, voltaje_vertical)
    )
    
    return voltaje_vertical

def generar_senal_horizontal(tiempo, frecuencia_horizontal, fase_horizontal, amplitud_horizontal):
    """
    Genera el voltaje sinusoidal para las placas de deflexion horizontal.
    V_horizontal(t) = A * sin(2π * f * t + φ)
    
    CORREGIDO: fase_horizontal se espera en RADIANES
    """
    if not validar_frecuencia(frecuencia_horizontal):
        raise ValueError(f"Frecuencia horizontal fuera de rango: {frecuencia_horizontal}")
        
    if not validar_amplitud_horizontal(amplitud_horizontal):
        raise ValueError(f"Amplitud horizontal fuera de rango: {amplitud_horizontal}")
    
    # IMPORTANTE: tiempo debe empezar desde 0 para figuras correctas
    # Calcular voltaje sinusoidal - fase ya en radianes
    voltaje_horizontal = amplitud_horizontal * math.sin(
        2 * math.pi * frecuencia_horizontal * tiempo + fase_horizontal
    )
    
    # Asegurar que este dentro de los limites de voltaje
    voltaje_horizontal = max(
        crt_parameters.VOLTAJE_HORIZONTAL_MIN, 
        min(crt_parameters.VOLTAJE_HORIZONTAL_MAX, voltaje_horizontal)
    )
    
    return voltaje_horizontal

#-------------------------------------------------------------------------------------
# PRESETS CORREGIDOS DE FIGURAS DE LISSAJOUS SEGÚN EL DOCUMENTO
#-------------------------------------------------------------------------------------
def obtener_presets_lissajous():
    """
    Devuelve configuraciones predefinidas para generar Figuras de Lissajous clasicas.
    CORREGIDO según el documento del proyecto y las fórmulas estándar.
    """
    presets = {
        'linea_diagonal': {
            'nombre': 'Línea Diagonal',
            'descripcion': 'Frecuencias iguales, sin desfase - δ=0',
            'frecuencia_vertical': 1.0,
            'fase_vertical': 0.0,                    # 0 grados
            'amplitud_vertical': 150,
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': 0.0,                  # 0 grados = línea diagonal
            'amplitud_horizontal': 150,
            'ratio': '1:1'
        },
        'elipse': {
            'nombre': 'Elipse',
            'descripcion': 'Frecuencias iguales, fase de π/4 - δ=π/4',
            'frecuencia_vertical': 1.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 150,
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': math.pi / 4,          # π/4 = 45 grados
            'amplitud_horizontal': 150,
            'ratio': '1:1'
        },
        'circulo': {
            'nombre': 'Círculo',
            'descripcion': 'Frecuencias iguales, fase de π/2 - δ=π/2',
            'frecuencia_vertical': 1.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 150,                # Amplitudes iguales para círculo perfecto
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': math.pi / 2,          # π/2 = 90 grados para círculo
            'amplitud_horizontal': 150,
            'ratio': '1:1'
        },
        'elipse_3pi4': {
            'nombre': 'Elipse 3π/4',
            'descripcion': 'Frecuencias iguales, fase de 3π/4 - δ=3π/4',
            'frecuencia_vertical': 1.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 150,
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': 3 * math.pi / 4,      # 3π/4 = 135 grados
            'amplitud_horizontal': 150,
            'ratio': '1:1'
        },
        'linea_horizontal': {
            'nombre': 'Línea Horizontal',
            'descripcion': 'Frecuencias iguales, fase de π - δ=π',
            'frecuencia_vertical': 1.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 150,
            'frecuencia_horizontal': 1.0,
            'fase_horizontal': math.pi,              # π = 180 grados
            'amplitud_horizontal': 150,
            'ratio': '1:1'
        },
        'ocho_vertical': {
            'nombre': 'Ocho Vertical (1:2)',
            'descripcion': 'Relación 1:2 vertical - δ=0',
            'frecuencia_vertical': 1.0,              # Base
            'fase_vertical': 0.0,
            'amplitud_vertical': 150,
            'frecuencia_horizontal': 2.0,            # Doble frecuencia
            'fase_horizontal': 0.0,                  # Sin desfase
            'amplitud_horizontal': 150,
            'ratio': '1:2'
        },
        'ocho': {
            'nombre': 'Ocho Horizontal (2:1)', 
            'descripcion': 'Relación 2:1 horizontal - δ=0',
            'frecuencia_vertical': 2.0,              # Doble frecuencia
            'fase_vertical': 0.0,
            'amplitud_vertical': 150,
            'frecuencia_horizontal': 1.0,            # Base
            'fase_horizontal': 0.0,                  # Sin desfase
            'amplitud_horizontal': 150,
            'ratio': '2:1'
        },
        'trebol_3_1': {
            'nombre': 'Trébol (3:1)',
            'descripcion': 'Relación 3:1 - δ=0',
            'frecuencia_vertical': 3.0,              # Triple frecuencia
            'fase_vertical': 0.0,
            'amplitud_vertical': 150,
            'frecuencia_horizontal': 1.0,            # Base
            'fase_horizontal': 0.0,                  # Sin desfase
            'amplitud_horizontal': 150,
            'ratio': '3:1'
        },
        'trebol': {
            'nombre': 'Trébol (1:3)',
            'descripcion': 'Relación 1:3 - δ=0',
            'frecuencia_vertical': 1.0,              # Base
            'fase_vertical': 0.0,
            'amplitud_vertical': 150,
            'frecuencia_horizontal': 3.0,            # Triple frecuencia
            'fase_horizontal': 0.0,                  # Sin desfase
            'amplitud_horizontal': 150,
            'ratio': '1:3'
        },
        'mariposa': {
            'nombre': 'Mariposa (3:2)',
            'descripcion': 'Relación 3:2 con desfase π/2',
            'frecuencia_vertical': 3.0,
            'fase_vertical': 0.0,
            'amplitud_vertical': 150,
            'frecuencia_horizontal': 2.0,
            'fase_horizontal': math.pi / 2,          # π/2 para patrón complejo
            'amplitud_horizontal': 150,
            'ratio': '3:2'
        }
    }
    
    return presets

#-------------------------------------------------------------------------------------
# FUNCIÓN CORREGIDA PARA GENERAR VOLTAJES LISSAJOUS
#-------------------------------------------------------------------------------------
def generar_voltajes_lissajous(tiempo, config_lissajous):
    """
    Genera ambos voltajes simultaneamente para crear una Figura de Lissajous.
    
    CORREGIDO: 
    - Manejo correcto de fases
    - Tiempo normalizado desde 0
    - Validaciones mejoradas
    """
    try:
        # Validar configuración
        required_keys = ['frecuencia_vertical', 'fase_vertical', 'amplitud_vertical',
                        'frecuencia_horizontal', 'fase_horizontal', 'amplitud_horizontal']
        
        for key in required_keys:
            if key not in config_lissajous:
                raise ValueError(f"Falta parámetro en configuración: {key}")
        
        # IMPORTANTE: Asegurar que el tiempo sea >= 0
        tiempo_normalizado = max(0, tiempo)
        
        voltaje_vertical = generar_senal_vertical(
            tiempo_normalizado,
            config_lissajous['frecuencia_vertical'],
            config_lissajous['fase_vertical'],      # Ya debe estar en radianes
            config_lissajous['amplitud_vertical']
        )
        
        voltaje_horizontal = generar_senal_horizontal(
            tiempo_normalizado,
            config_lissajous['frecuencia_horizontal'],
            config_lissajous['fase_horizontal'],    # Ya debe estar en radianes
            config_lissajous['amplitud_horizontal']
        )
        
        return {
            'voltaje_vertical': voltaje_vertical,
            'voltaje_horizontal': voltaje_horizontal,
            'tiempo': tiempo_normalizado,
            'debug_info': {
                'config_usado': config_lissajous,
                'tiempo_original': tiempo,
                'tiempo_normalizado': tiempo_normalizado
            }
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'voltaje_vertical': 0,
            'voltaje_horizontal': 0,
            'tiempo': tiempo
        }

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

#-------------------------------------------------------------------------------------
# FUNCIÓN PARA OBTENER PRESET ESPECÍFICO POR RATIO
#-------------------------------------------------------------------------------------
def obtener_preset_por_ratio(ratio_vertical, ratio_horizontal, fase_desfase=0):
    """
    Genera configuración de Lissajous para un ratio específico.
    
    Args:
        ratio_vertical: Multiplicador de frecuencia vertical (ej: 1, 2, 3)
        ratio_horizontal: Multiplicador de frecuencia horizontal (ej: 1, 2, 3) 
        fase_desfase: Desfase en radianes (ej: 0, π/4, π/2, π)
    """
    frecuencia_base = 1.0
    
    config = {
        'frecuencia_vertical': frecuencia_base * ratio_vertical,
        'fase_vertical': 0.0,  # Siempre empezar vertical en 0
        'amplitud_vertical': 150,
        'frecuencia_horizontal': frecuencia_base * ratio_horizontal,
        'fase_horizontal': fase_desfase,  # Aplicar desfase al horizontal
        'amplitud_horizontal': 150,
        'ratio_string': f"{ratio_vertical}:{ratio_horizontal}",
        'fase_grados': fase_desfase * 180 / math.pi
    }
    
    return config

#-------------------------------------------------------------------------------------
# FUNCIÓN DE DEBUG PARA VERIFICAR CONFIGURACIONES
#-------------------------------------------------------------------------------------
def debug_preset_lissajous(nombre_preset):
    """
    Función de debug para verificar que los presets estén correctos.
    """
    presets = obtener_presets_lissajous()
    
    if nombre_preset not in presets:
        return {'error': f'Preset no encontrado: {nombre_preset}'}
    
    preset = presets[nombre_preset]
    
    # Generar algunos puntos de muestra
    puntos_muestra = []
    for t in [0, 0.25, 0.5, 0.75, 1.0]:
        voltajes = generar_voltajes_lissajous(t, preset)
        puntos_muestra.append({
            'tiempo': t,
            'voltajes': voltajes
        })
    
    return {
        'preset': preset,
        'puntos_muestra': puntos_muestra,
        'fase_vertical_grados': preset['fase_vertical'] * 180 / math.pi,
        'fase_horizontal_grados': preset['fase_horizontal'] * 180 / math.pi
    }