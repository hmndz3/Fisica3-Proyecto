#-------------------------------------------------------------------------------------
# APLICACION PRINCIPAL FLASK PARA EL SIMULADOR CRT
# Esta aplicacion conecta el backend de calculos fisicos con el frontend web
# Proporciona APIs REST para todos los calculos del CRT y sirve la interfaz web
#-------------------------------------------------------------------------------------

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import time
import math

# Importar nuestros modulos de calculos fisicos
from crt_parameters import *
from electron_motion import *
from lissajous_generator import *

#-------------------------------------------------------------------------------------
# CONFIGURACION DE LA APLICACION FLASK
#-------------------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)  # Permitir CORS para desarrollo

# Configuracion para desarrollo
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'crt_simulator_2025'

#-------------------------------------------------------------------------------------
# VARIABLES GLOBALES PARA ESTADO DE LA SIMULACION
#-------------------------------------------------------------------------------------
# Estado actual de los voltajes (modo manual)
estado_voltajes = {
    'voltaje_aceleracion': VOLTAJE_ACELERACION_DEFAULT,
    'voltaje_vertical': VOLTAJE_VERTICAL_DEFAULT,
    'voltaje_horizontal': VOLTAJE_HORIZONTAL_DEFAULT,
    'tiempo_persistencia': TIEMPO_PERSISTENCIA_DEFAULT
}

# Estado actual de Lissajous (modo automatico)
estado_lissajous = obtener_configuracion_default_lissajous()

# Modo de operacion: 'manual' o 'lissajous'
modo_operacion = 'manual'

# Tiempo de inicio para animaciones
tiempo_inicio_animacion = time.time()

#-------------------------------------------------------------------------------------
# RUTA PRINCIPAL - INTERFAZ WEB
#-------------------------------------------------------------------------------------
@app.route('/')
def index():
    """Sirve la pagina principal del simulador."""
    return render_template('index.html')

#-------------------------------------------------------------------------------------
# APIS PARA PARAMETROS DEL SISTEMA
#-------------------------------------------------------------------------------------
@app.route('/api/parametros-sistema', methods=['GET'])
def obtener_parametros_sistema_api():
    """Devuelve todos los parametros fijos del sistema CRT."""
    try:
        parametros = obtener_parametros_sistema()
        return jsonify({
            'success': True,
            'data': parametros
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/info-lissajous', methods=['GET'])
def obtener_info_lissajous_api():
    """Devuelve informacion sobre parametros de Lissajous."""
    try:
        info = obtener_info_lissajous()
        return jsonify({
            'success': True,
            'data': info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

#-------------------------------------------------------------------------------------
# APIS PARA MODO MANUAL
#-------------------------------------------------------------------------------------
@app.route('/api/actualizar-voltajes', methods=['POST'])
def actualizar_voltajes_api():
    """Actualiza los voltajes en modo manual."""
    global estado_voltajes, modo_operacion
    
    try:
        datos = request.get_json()
        
        # Cambiar a modo manual
        modo_operacion = 'manual'
        
        # Validar y actualizar voltaje de aceleracion
        if 'voltaje_aceleracion' in datos:
            voltaje = float(datos['voltaje_aceleracion'])
            if validar_voltaje_aceleracion(voltaje):
                estado_voltajes['voltaje_aceleracion'] = voltaje
            else:
                return jsonify({
                    'success': False,
                    'error': f'Voltaje de aceleracion fuera de rango: {voltaje}'
                }), 400
        
        # Validar y actualizar voltaje vertical
        if 'voltaje_vertical' in datos:
            voltaje = float(datos['voltaje_vertical'])
            if validar_voltaje_vertical(voltaje):
                estado_voltajes['voltaje_vertical'] = voltaje
            else:
                return jsonify({
                    'success': False,
                    'error': f'Voltaje vertical fuera de rango: {voltaje}'
                }), 400
        
        # Validar y actualizar voltaje horizontal
        if 'voltaje_horizontal' in datos:
            voltaje = float(datos['voltaje_horizontal'])
            if validar_voltaje_horizontal(voltaje):
                estado_voltajes['voltaje_horizontal'] = voltaje
            else:
                return jsonify({
                    'success': False,
                    'error': f'Voltaje horizontal fuera de rango: {voltaje}'
                }), 400
        
        # Validar y actualizar tiempo de persistencia
        if 'tiempo_persistencia' in datos:
            tiempo = float(datos['tiempo_persistencia'])
            if validar_tiempo_persistencia(tiempo):
                estado_voltajes['tiempo_persistencia'] = tiempo
            else:
                return jsonify({
                    'success': False,
                    'error': f'Tiempo de persistencia fuera de rango: {tiempo}'
                }), 400
        
        return jsonify({
            'success': True,
            'data': estado_voltajes,
            'modo': modo_operacion
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/calcular-posicion', methods=['POST'])
def calcular_posicion_api():
    """Calcula la posicion del electron en la pantalla."""
    try:
        datos = request.get_json()
        
        # Usar voltajes proporcionados o los del estado actual
        voltaje_aceleracion = datos.get('voltaje_aceleracion', estado_voltajes['voltaje_aceleracion'])
        voltaje_vertical = datos.get('voltaje_vertical', estado_voltajes['voltaje_vertical'])
        voltaje_horizontal = datos.get('voltaje_horizontal', estado_voltajes['voltaje_horizontal'])
        
        # Calcular posicion final
        resultado = calcular_posicion_final_electron(
            voltaje_aceleracion, voltaje_vertical, voltaje_horizontal
        )
        
        return jsonify({
            'success': True,
            'data': resultado,
            'voltajes_usados': {
                'voltaje_aceleracion': voltaje_aceleracion,
                'voltaje_vertical': voltaje_vertical,
                'voltaje_horizontal': voltaje_horizontal
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

#-------------------------------------------------------------------------------------
# APIS PARA MODO LISSAJOUS
#-------------------------------------------------------------------------------------
@app.route('/api/configurar-lissajous', methods=['POST'])
def configurar_lissajous_api():
    """Configura los parametros para generar Figuras de Lissajous."""
    global estado_lissajous, modo_operacion, tiempo_inicio_animacion
    
    try:
        datos = request.get_json()
        
        # Cambiar a modo Lissajous
        modo_operacion = 'lissajous'
        
        # Reiniciar tiempo de animacion
        tiempo_inicio_animacion = time.time()
        
        # Actualizar configuracion de Lissajous
        estado_lissajous = actualizar_parametros_lissajous(estado_lissajous, datos)
        
        return jsonify({
            'success': True,
            'data': estado_lissajous,
            'modo': modo_operacion
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/aplicar-preset-lissajous', methods=['POST'])
def aplicar_preset_lissajous_api():
    """Aplica un preset predefinido de Figura de Lissajous."""
    global estado_lissajous, modo_operacion, tiempo_inicio_animacion
    
    try:
        datos = request.get_json()
        nombre_preset = datos.get('preset')
        
        if not nombre_preset:
            return jsonify({
                'success': False,
                'error': 'No se especifico el preset'
            }), 400
        
        # Obtener presets disponibles
        presets = obtener_presets_lissajous()
        
        if nombre_preset not in presets:
            return jsonify({
                'success': False,
                'error': f'Preset no encontrado: {nombre_preset}'
            }), 400
        
        # Cambiar a modo Lissajous
        modo_operacion = 'lissajous'
        
        # Reiniciar tiempo de animacion
        tiempo_inicio_animacion = time.time()
        
        # Aplicar preset
        preset = presets[nombre_preset]
        estado_lissajous = {
            'frecuencia_vertical': preset['frecuencia_vertical'],
            'fase_vertical': preset['fase_vertical'],
            'amplitud_vertical': preset['amplitud_vertical'],
            'frecuencia_horizontal': preset['frecuencia_horizontal'],
            'fase_horizontal': preset['fase_horizontal'],
            'amplitud_horizontal': preset['amplitud_horizontal']
        }
        
        return jsonify({
            'success': True,
            'data': estado_lissajous,
            'preset_aplicado': preset,
            'modo': modo_operacion
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voltajes-lissajous-tiempo-real', methods=['GET'])
def obtener_voltajes_lissajous_tiempo_real():
    """Obtiene los voltajes actuales de Lissajous basados en el tiempo transcurrido."""
    global tiempo_inicio_animacion, estado_lissajous, estado_voltajes
    
    try:
        if modo_operacion != 'lissajous':
            return jsonify({
                'success': False,
                'error': 'No se encuentra en modo Lissajous'
            }), 400
        
        # Calcular tiempo transcurrido desde el inicio de la animacion
        tiempo_actual = time.time() - tiempo_inicio_animacion
        
        # Generar voltajes para este momento
        voltajes = generar_voltajes_lissajous(tiempo_actual, estado_lissajous)
        
        if 'error' in voltajes:
            return jsonify({
                'success': False,
                'error': voltajes['error']
            }), 500
        
        # Calcular posicion del electron con estos voltajes
        posicion = calcular_posicion_final_electron(
            estado_voltajes['voltaje_aceleracion'],
            voltajes['voltaje_vertical'],
            voltajes['voltaje_horizontal']
        )
        
        return jsonify({
            'success': True,
            'data': {
                'voltajes': voltajes,
                'posicion': posicion,
                'tiempo_transcurrido': tiempo_actual,
                'config_lissajous': estado_lissajous
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

#-------------------------------------------------------------------------------------
# APIS DE CONTROL GENERAL
#-------------------------------------------------------------------------------------
@app.route('/api/cambiar-modo', methods=['POST'])
def cambiar_modo_api():
    """Cambia entre modo manual y modo Lissajous."""
    global modo_operacion, tiempo_inicio_animacion
    
    try:
        datos = request.get_json()
        nuevo_modo = datos.get('modo')
        
        if nuevo_modo not in ['manual', 'lissajous']:
            return jsonify({
                'success': False,
                'error': 'Modo invalido. Use "manual" o "lissajous"'
            }), 400
        
        modo_operacion = nuevo_modo
        
        # Si cambiamos a Lissajous, reiniciar tiempo
        if nuevo_modo == 'lissajous':
            tiempo_inicio_animacion = time.time()
        
        return jsonify({
            'success': True,
            'data': {
                'modo': modo_operacion,
                'estado_voltajes': estado_voltajes,
                'estado_lissajous': estado_lissajous
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/estado-actual', methods=['GET'])
def obtener_estado_actual():
    """Obtiene el estado actual completo del simulador."""
    try:
        return jsonify({
            'success': True,
            'data': {
                'modo': modo_operacion,
                'voltajes': estado_voltajes,
                'lissajous': estado_lissajous,
                'tiempo_desde_inicio': time.time() - tiempo_inicio_animacion if modo_operacion == 'lissajous' else 0
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

#-------------------------------------------------------------------------------------
# MANEJO DE ERRORES
#-------------------------------------------------------------------------------------
@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404

@app.errorhandler(500)
def error_interno(error):
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500

#-------------------------------------------------------------------------------------
# PUNTO DE ENTRADA DE LA APLICACION
#-------------------------------------------------------------------------------------
if __name__ == '__main__':
    print("🚀 Iniciando Simulador CRT...")
    print("📡 Backend: Calculos fisicos listos")
    print("🌐 Frontend: http://localhost:5000")
    print("📊 APIs disponibles en /api/")
    
    app.run(host='0.0.0.0', port=5000, debug=True)