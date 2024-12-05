# client/utils.py

import coincurve
from coincurve import PrivateKey
import os

def generate_keys():
    """
    Genera un par de claves privada y pública.
    """
    private_key = PrivateKey()
    public_key = private_key.public_key
    return private_key, public_key

def serialize_public_key(public_key):
    """
    Serializa la clave pública en formato hexadecimal.
    """
    return public_key.format(compressed=True).hex()

def sign_challenge(private_key, challenge_int):
    """
    Firma el desafío utilizando la clave privada con firmas Schnorr.
    """
    message = str(challenge_int).encode()
    signature = private_key.schnorr_sign(message)  # Corrección aquí
    return signature.hex()

def load_private_key(filepath):
    """
    Carga la clave privada desde un archivo hexadecimal.
    """
    if not os.path.exists(filepath):
        print(f"Archivo de clave privada no encontrado: {filepath}")
        return None
    with open(filepath, 'r') as f:
        private_hex = f.read().strip()
    try:
        return PrivateKey(bytes.fromhex(private_hex))
    except ValueError as e:
        print(f"Error al cargar la clave privada: {e}")
        return None
