# client/client.py

import requests
import json
import os
from utils import generate_keys, serialize_public_key, sign_challenge, load_private_key

SERVER_URL = 'http://localhost:5001'

def register_user():
    username = input("Ingrese su nombre de usuario: ")

    # Generar claves
    private_key, public_key = generate_keys()
    public_hex = serialize_public_key(public_key)

    # Enviar clave pública al servidor
    payload = {
        'username': username,
        'public_key': public_hex
    }

    try:
        response = requests.post(f"{SERVER_URL}/register", json=payload)
        response.raise_for_status()  # Levanta un error para códigos de estado HTTP 4xx/5xx
    except requests.exceptions.RequestException as e:
        print(f"Error al conectarse al servidor: {e}")
        return

    try:
        data = response.json()
        if response.status_code == 200:
            print("Registro exitoso.")
            # Guardar la clave privada localmente en formato hexadecimal
            with open(f"{username}_private_key.hex", "w") as f:
                f.write(private_key.to_hex())
            print(f"Clave privada guardada como {username}_private_key.hex")
        else:
            print(f"Error en el registro: {data.get('message')}")
    except json.decoder.JSONDecodeError:
        print(f"Respuesta no válida del servidor: {response.text}")

def authenticate_user():
    username = input("Ingrese su nombre de usuario: ")

    # Generar un desafío (challenge)
    challenge_int = generate_challenge()
    print(f"Desafío generado: {challenge_int}")

    # Cargar la clave privada
    private_key = load_private_key(f"{username}_private_key.hex")
    if not private_key:
        print("Clave privada no encontrada o inválida. Por favor, registra el usuario primero.")
        return

    # Firmar el desafío
    try:
        response_signature = sign_challenge(private_key, challenge_int)
    except AttributeError as e:
        print(f"Error al firmar el desafío: {e}")
        return

    # Enviar la firma al servidor para autenticar
    payload = {
        'username': username,
        'challenge': challenge_int,
        'response': response_signature
    }

    try:
        response = requests.post(f"{SERVER_URL}/authenticate", json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectarse al servidor: {e}")
        return

    try:
        data = response.json()
        if response.status_code == 200:
            print("Autenticación exitosa.")
        else:
            print(f"Error en la autenticación: {data.get('message')}")
    except json.decoder.JSONDecodeError:
        print(f"Respuesta no válida del servidor: {response.text}")

def generate_challenge():
    """
    Genera un número aleatorio como desafío.
    """
    import random
    return random.randint(10**15, 10**19)  # Número aleatorio de 16 a 19 dígitos

def main():
    while True:
        print("\nSeleccione una opción:")
        print("1. Registrar Usuario")
        print("2. Autenticar Usuario")
        print("3. Salir")
        choice = input("Ingrese 1, 2 o 3: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            authenticate_user()
        elif choice == '3':
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Por favor, ingrese 1, 2 o 3.")

if __name__ == '__main__':
    main()
