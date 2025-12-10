# app.py
from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)
# Directorio donde se almacenarán los archivos
FILE_DIR = 'data'

# Asegurarse de que el directorio exista
if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)

# --- Funciones Auxiliares ---
def get_file_path(filename):
    """Devuelve la ruta completa al archivo dentro del directorio de datos."""
    return os.path.join(FILE_DIR, filename)

# --- Rutas de la API ---

# 1. GET (Leer/Enviar Archivo)
@app.route('/archivo/<filename>', methods=['GET'])
def get_file(filename):
    file_path = get_file_path(filename)
    
    if not os.path.exists(file_path):
        return jsonify({"error": "Archivo no encontrado"}), 404
        
    try:
        # Usamos send_file para enviar el archivo directamente
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": f"Error al leer el archivo: {str(e)}"}), 500

# app.py (SOLO MODIFICA esta función)

# 2. POST (Crear/Sobrescribir Archivo)
@app.route('/archivo/<filename>', methods=['POST'])
def create_file(filename):
    file_path = get_file_path(filename)
    content = ""
    
    # --- Lógica Mejorada para Extraer Contenido ---
    if request.is_json:
        # Si el cliente envía JSON (e.g., {"content": "mi texto"})
        data = request.get_json()
        content = data.get('content', '') # Extrae el valor de la clave 'content'
    elif request.data:
        # Si el cliente envía texto plano/crudo (raw body)
        content = request.data.decode('utf-8')
    # --- Fin Lógica Mejorada ---

    if not content:
        return jsonify({"error": "No se recibió contenido para escribir en el archivo."}), 400

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        # 201 Created (Creado)
        return jsonify({"message": f"Archivo '{filename}' creado/actualizado exitosamente."}), 201 
    except Exception as e:
        return jsonify({"error": f"Error al escribir en el archivo: {str(e)}"}), 500

# 3. DELETE (Eliminar Archivo)
@app.route('/archivo/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = get_file_path(filename)
    
    if not os.path.exists(file_path):
        return jsonify({"error": "Archivo no encontrado"}), 404
    
    try:
        os.remove(file_path)
        return jsonify({"message": f"Archivo '{filename}' eliminado exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el archivo: {str(e)}"}), 500

if __name__ == '__main__':
    # Ejecuta el servidor de desarrollo de Flask
    # En producción, usarías un servidor como Gunicorn o Waitress
    app.run(debug=True)