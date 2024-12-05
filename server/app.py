# server/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from utils import load_public_key, verify_response

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir solicitudes desde el cliente

# Ruta para almacenar usuarios
USERS_FILE = 'users.json'

# Cargar usuarios desde el archivo JSON
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error: users.json está malformado. Inicializando con un objeto vacío.")
                return {}
    return {}

# Guardar usuarios en el archivo JSON
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/register', methods=['POST'])
def register():
    print("Recibida solicitud de registro")
    data = request.get_json()
    username = data.get('username')
    public_key_hex = data.get('public_key')

    if not username or not public_key_hex:
        print("Datos incompletos en registro")
        return jsonify({'message': 'Datos incompletos'}), 400

    users = load_users()

    if username in users:
        print(f"El usuario {username} ya está registrado")
        return jsonify({'message': 'El usuario ya está registrado'}), 400

    # Guardar la clave pública
    users[username] = {
        'public_key': public_key_hex
    }

    save_users(users)
    print(f"Usuario {username} registrado exitosamente")

    return jsonify({'message': 'Usuario registrado exitosamente'}), 200

@app.route('/authenticate', methods=['POST'])
def authenticate():
    print("Recibida solicitud de autenticación")
    data = request.get_json()
    username = data.get('username')
    challenge = data.get('challenge')
    response = data.get('response')

    if not username or challenge is None or response is None:
        print("Datos incompletos en autenticación")
        return jsonify({'message': 'Datos incompletos'}), 400

    users = load_users()

    if username not in users:
        print(f"Usuario {username} no encontrado")
        return jsonify({'message': 'Usuario no encontrado'}), 404

    public_key_hex = users[username]['public_key']

    # Cargar la clave pública
    public_key = load_public_key(public_key_hex)

    # Verificar la respuesta
    is_valid = verify_response(public_key, challenge, response)
    print(f"Verificación de respuesta: {'válida' if is_valid else 'inválida'}")

    if is_valid:
        return jsonify({'message': 'Autenticación exitosa'}), 200
    else:
        return jsonify({'message': 'Autenticación fallida'}), 400

# Manejo de errores inesperados
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Error inesperado: {e}")
    return jsonify({'message': 'Ocurrió un error inesperado.'}), 500

if __name__ == '__main__':
    print("Iniciando servidor Flask en 0.0.0.0:5001")
    app.run(host='0.0.0.0', port=5001)
